import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from dialogflow_payload_gen.csv_parser_xl import CSVParserXL

from dialogflow import Dialogflow


from datetime import datetime
import graphviz


class Visualizer:
    def __init__(self, config: dict) -> None:

        self.configure(config)

        self._parser = CSVParserXL(self.config)
        self._parser.load(filepath=self.config["parse_filepath"])
        self._api = Dialogflow(self.config)

        self._graphs = []

        self.create()

    def configure(self, config: dict):
        self.config = config

    def create(self):
        """ """
        self._api.get_intents()
        self._api.generate_tree()

        self.create_record()

    def create_record(self):
        """ """
        root_intents = self._api.get_root_intents()
        exportable_intents = self.get_exportable_root_intents()

        languages = self.config["sheet_data"].get("languages", ["english"])

        for language in languages:
            for root_intent in root_intents:

                if root_intent.display_name not in exportable_intents:
                    continue

                graph = graphviz.Digraph(
                    name=f"{root_intent.display_name}",
                    directory=self.get_render_path(root_intent.display_name, language),
                    filename=f"{root_intent.display_name}.gv",
                    edge_attr={},
                    graph_attr={},
                    node_attr={
                        "shape": "plaintext",
                    },
                    format="pdf",
                    engine="dot",
                    formatter="cairo",
                    renderer="cairo",
                )

                def create_edge(node):
                    intent = node.intent_obj

                    self.create_record_node(graph, node, language)

                    if intent.action:
                        action = self._api.intents["display_name"].get(
                            intent.action, None
                        )
                        if action:
                            edge_style = self.config["style_data"]["edge"]["indirect"]
                            graph.edge(
                                f"{intent.display_name}",
                                f"{action.display_name}",
                                color=edge_style["color"],
                                style=edge_style["style"],
                                arrowsize=edge_style["arrowsize"],
                                penwidth=edge_style["penwidth"],
                            )

                    if node.parent:
                        parent = node.parent.intent_obj
                        edge_style = self.config["style_data"]["edge"]["direct"]
                        graph.edge(
                            f"{parent.display_name}",
                            f"{intent.display_name}",
                            color=edge_style["color"],
                            style=edge_style["style"],
                            arrowsize=edge_style["arrowsize"],
                            penwidth=edge_style["penwidth"],
                        )
                    else:
                        pass

                    for child in node.children:
                        create_edge(child)

                create_edge(root_intent)

                graph.render(
                    # filename=f"{intent.display_name}.gv",
                    # directory=f"{os.path.abspath(self.config['render_path'])}/{datetime.now().strftime('%Y-%m-%d-%H:%M')}",
                    view=False,
                    # format="pdf",
                    # renderer="cairo",
                    # engine="dot",
                    # formatter="cairo",
                    outfile=os.path.join(
                        self.get_render_path(root_intent.display_name, language),
                        f"{root_intent.display_name}.pdf",
                    ),
                )
                self._graphs.append(graph)

    def get_render_path(self, intent_name: str, language: str = "english"):
        gid_mapping = self.config["sheet_data"]["gid_mapping"]

        path = os.path.abspath(self.config["render_path"])

        for day in gid_mapping:
            for session in gid_mapping[day]:
                intents = gid_mapping[day][session]["intents"]
                if intent_name in intents:
                    path = os.path.join(
                        os.path.abspath(self.config["render_path"]),
                        datetime.now().strftime("%Y-%m-%d-%H:%M"),
                        language.title(),
                        f"day-{day}".title(),
                        f"session-{session}".title(),
                    )
                    os.makedirs(path, exist_ok=True)
                    return path
        return path

    def get_exportable_root_intents(self) -> list:
        exportable_intentes = []

        gid_mapping = self.config["sheet_data"]["gid_mapping"]
        for day in gid_mapping:
            for session in gid_mapping[day]:
                intents = gid_mapping[day][session]["intents"]
                exportable_intentes.extend(intents)

        return exportable_intentes

    def get_url(self, node, language):
        intent_name = node.display_name
        sheet_data = self.config["sheet_data"]

        url = ""

        def get_sheet_mapping(name: str) -> tuple:
            """ """

            def get_sheet_name(day: str, session: str) -> str:
                return f"day-{day}-session-{session}"

            gid = ""
            sheet_name = ""

            # name = name.replace("topic-", "").replace(" ", "-").strip().lower()
            gid_mapping = self.config["sheet_data"]["gid_mapping"]
            for day in gid_mapping:
                for session in gid_mapping[day]:
                    intents = gid_mapping[day][session]["intents"]
                    if name in intents:
                        gid = gid_mapping[day][session]["gid"]
                        sheet_name = get_sheet_name(day, session)
                        return sheet_name, gid

            return sheet_name, gid

        def get_response_indices(intents: list, intent_name: str) -> tuple:
            intent_rows = [
                x
                for x in intents
                if x[self._parser._header_map["intent"]] == intent_name
            ]
            start_idx = intents.index(next(iter(intent_rows))) + 2
            end_idx = start_idx + len(intent_rows) - 1

            return start_idx, end_idx

        try:
            sheet_name, gid = get_sheet_mapping(node.root.display_name)
            intents = self._parser._data_sheets[sheet_name]
            start_idx, end_idx = get_response_indices(intents, intent_name)

            url = f"{sheet_data['base_url'][language]}gid={gid}&amp;range={sheet_data['range_column']['start']}{start_idx}:{sheet_data['range_column']['end']}{end_idx}"

        except Exception as e:
            pass

        return url

    def create_record_node(self, graph, node, language: str):

        record_def = ""

        style_data = (
            self.config["style_data"]["fallback"]
            if node.intent_obj.is_fallback
            else self.config["style_data"]["default"]
        )

        url = self.get_url(node, language)

        record_def += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="intent_name" COLSPAN="2" STYLE="ROUNDED" BGCOLOR="{style_data['intent-name']['color']}" CELLPADDING="30" HREF="{url}"><FONT POINT-SIZE="{style_data['intent-name']['font-size']}" FACE="{style_data['intent-name']['font']}"><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

        # if node.intent_obj.action:
        #     record_def += f"""
        # <TR>
        #     <TD BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
        #     <TD PORT="action" BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['action']['font-size']}" FACE="{style_data['action']['font']}">{node.intent_obj.action}</FONT></TD>
        # </TR>
        # """

        if node.has_text_messages:

            for i, responses in enumerate(node.text_messages):
                if i > 0:
                    record_def += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="black" CELLPADDING="5" STYLE="ROUNDED"></TD>
        </TR>
        """
                for j, paraphrase in enumerate(responses):
                    record_def += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="{style_data['messages']['color']}" CELLPADDING="20" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['messages']['font-size']}" FACE="{style_data['messages']['font']}"><i>{paraphrase}</i></FONT></TD>
        </TR>
        """

        record_def += f"""
        </TABLE>
        """

        graph.node(node.display_name, f"<{record_def}>")

    def view(self):
        for graph in self._graphs:
            graph.view()


if __name__ == "__main__":

    sheet_data = {
        "languages": ["english", "spanish"],
        # Actual
        "base_url": {
            "english": "https://docs.google.com/spreadsheets/d/16jQ8q7M72dBdkxpcIKPXT1nRQbmD4wibZIQRgN_84X8/edit#",
            "spanish": "https://docs.google.com/spreadsheets/d/1-VE3Rw25G_Z3DKpYPCcg-jmix3oUf2JdVMDLR6FJhOs/edit#",
        },
        # Test
        # "base_url": "https://docs.google.com/spreadsheets/d/1kMeUTg8ewt-mtUago2ld7hG92vm1GBdT/edit#",
        "parameters": ["gid", "range"],
        "gid_mapping": {
            "1": {
                "1": {
                    "gid": "1163585192",
                    "intents": [
                        "topic-intro",
                        "topic-day-one-session-one-names-origins",
                        "topic-day-one-session-one-transition-age",
                        "topic-day-one-session-one-age",
                    ],
                },
                "2": {
                    "gid": "919985165",
                    "intents": [
                        "topic-day-one-session-two-intro",
                        "topic-travel-homecountry",
                        "topic-day-one-session-two-transition",
                        "topic-hometown",
                        "topic-day-one-session-two-outro",
                    ],
                },
            },
            "2": {
                "1": {
                    "gid": "743627153",
                    "intents": [
                        "topic-day-two-session-one-intro",
                        "topic-day-two-family",
                        "topic-day-two-session-one-transition",
                        "topic-day-two-parents",
                        "topic-day-two-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "2061915944",
                    "intents": [
                        "topic-day-two-session-two-intro",
                        "topic-pet-new",
                        "topic-day-two-session-two-transition",
                        "topic-lemurs",
                        "topic-day-two-session-two-end",
                    ],
                },
            },
            "3": {
                "1": {
                    "gid": "81336119",
                    "intents": [
                        "topic-day-three-session-one-intro",
                        "topic-day-three-food",
                        "topic-day-three-session-one-transition",
                        "topic-birthday",
                        "topic-day-three-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "1627598687",
                    "intents": [
                        "topic-day-three-session-two-intro",
                        "topic-sports",
                        "topic-day-three-session-two-transition",
                        "topic-day-three-hobbies",
                        "topic-day-three-session-two-outro",
                    ],
                },
            },
            "4": {
                "1": {
                    "gid": "592896325",
                    "intents": [
                        "topic-day-four-session-one-intro",
                        "topic-day-four-school",
                        "topic-day-four-session-one-transition",
                        "topic-day-four-friends",
                        "topic-day-four-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "804812225",
                    "intents": [
                        "topic-day-four-session-two-intro",
                        "topic-language",
                        "topic-day-four-session-two-transition",
                        "topic-music",
                        "topic-day-four-session-two-outro",
                    ],
                },
            },
            "5": {
                "1": {
                    "gid": "1381156119",
                    "intents": [
                        "topic-day-five-session-one-intro",
                        "topic-day-five-weather",
                        "topic-day-five-session-one-transition",
                        "topic-day-five-clothing",
                        "topic-day-five-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "148830916",
                    "intents": [
                        "topic-day-five-session-two-intro",
                        "topic-day-five-travel",
                        "topic-day-five-session-two-transition",
                        "topic-olympics",
                        "topic-day-five-session-two-outro",
                    ],
                },
                "3": {
                    "gid": "2048883617",
                    "intents": [
                        "topic-day-five-session-three-intro",
                        "topic-day-five-session-three-poem",
                        "topic-day-five-session-three-outro",
                    ],
                },
            },
        },
        "range_column": {
            "start": "B",
            "end": "K",
        },
    }

    style_data = {
        "default": {
            "intent-name": {
                "color": "darkcyan",
                "font-size": "20",
                "font": "Calibri",
            },
            "action": {
                "color": "darkseagreen4",
                "font-size": "16",
                "font": "Calibri",
            },
            "messages": {
                "color": "burlywood1",
                "font-size": "18",
                "font": "Calibri",
            },
        },
        "fallback": {
            "intent-name": {
                "color": "coral",
                "font-size": "20",
                "font": "Calibri",
            },
            "action": {
                "color": "darkseagreen4",
                "font-size": "16",
                "font": "Calibri",
            },
            "messages": {
                "color": "burlywood1",
                "font-size": "18",
                "font": "Calibri",
            },
        },
        "edge": {
            "direct": {
                "color": "black",
                "arrowsize": "2.0",
                "penwidth": "3.0",
                "style": "",
            },
            "indirect": {
                "color": "firebrick2",
                "arrowsize": "2.0",
                "penwidth": "3.0",
                "style": "",
            },
        }
        # "question": {
        #     "intent-name": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        #     "action": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        #     "messages": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        # },
        # "answer": {
        #     "intent-name": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        #     "action": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        #     "messages": {
        #         "color": "darkturquoise",
        #         "font-size": "20",
        #         "font": "Calibri",
        #     },
        # },
    }

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        "project_id": "empathetic-stimulator-owp9",
        "credential": f"{agent_dir}/es.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders",
        "sheet_data": sheet_data,
        "parse_filepath": f"{data_dir}/ES.xlsx",
        "style_data": style_data,
    }

    viz = Visualizer(config)
    # viz.view()
