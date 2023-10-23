import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from datetime import datetime

from dialogflow import Dialogflow, Intent
from dialogflow_payload_gen.csv_parser_xl import CSVParserXL

from graphviz import Digraph

from base_visualizer import BaseVisualizer
from node_definitions import get_node_def_basic


class HaruGamesVisualizer(BaseVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

        self._parser = CSVParserXL(self.config)
        self._parser.load(filepath=self.config["parse_filepath"])

    def load(self, language_code=None):
        return super().load(
            language_code if language_code else self.config.get("language_code", "en-us")
        )

    def create_graph(self, intents: list):
        """ """
        languages = self.config["sheet_data"].get("languages", ["english"])

        for language in languages:
            for intent in intents:
                intent: Intent
                graph = self.get_graph(
                    name=f"{intent.display_name}",
                    directory=self.get_render_path(
                        intent_name=intent.display_name, language=language
                    ),
                    filename=f"{intent.display_name}.gv",
                    format="pdf",
                )

                self.create_edge(graph, intent, language=language)

                graph.render(
                    # filename=f"{intent.display_name}.gv",
                    # directory=f"{os.path.abspath(self.config['render_path'])}/{datetime.now().strftime('%Y-%m-%d-%H:%M')}",
                    view=False,
                    # format="pdf",
                    # renderer="cairo",
                    # engine="dot",
                    # formatter="cairo",
                    outfile=os.path.join(
                        self.get_render_path(intent.display_name, language=language),
                        f"{intent.display_name}.pdf",
                    ),
                )
                self._graphs.append(graph)

    def create_edge(self, graph: Digraph, node: Intent, **kwargs):
        """ """
        intent = node.intent_obj

        graph.node(
            node.display_name,
            self.get_node_definition(
                node,
                **kwargs,
            ),
        )

        if intent.action:
            action = self._api.intents["display_name"].get(intent.action, None)
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
            self.create_edge(graph, child, **kwargs)

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

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        return get_node_def_basic(
            node,
            style_data=self.config["style_data"],
            url=self.get_url(node, kwargs["language"]),
        )


def get_exportable_root_intents(sheet_data: dict) -> list:
    exportable_intentes = []

    gid_mapping = sheet_data["gid_mapping"]
    for day in gid_mapping:
        for session in gid_mapping[day]:
            intents = gid_mapping[day][session]["intents"]
            exportable_intentes.extend(intents)

    return exportable_intentes


if __name__ == "__main__":

    sheet_data = {
        "languages": ["english", "spanish"],
        # Actual
        "base_url": {
            "english": "https://docs.google.com/spreadsheets/d/1jAAjXzTlJsE6mNvuHLU3dMDDkSlBM7_w_6wI-Mgjwds/edit#",
            # Test
            # "english": "https://docs.google.com/spreadsheets/d/1iPm9jG-CY1v_kh-ghS-pxzxGIcUkdUXF/edit#",
        },
        "parameters": ["gid", "range"],
        "gid_mapping": {
            "game-intros": {
                "gid": "",
                "intents": [],
            },
            "game-prompt": {
                "gid": "",
                "intents": [],
            },
            "game-pro": {
                "gid": "",
                "intents": [],
            },
            "game-intros": {
                "gid": "",
                "intents": [],
            },
            "game-intros": {
                "gid": "",
                "intents": [],
            },
            "game-intros": {
                "gid": "",
                "intents": [],
            },
            "game-intros": {
                "gid": "",
                "intents": [],
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
        # "project_id": "api-test-v99y",
        "credential": f"{agent_dir}/child-in-hospital.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders",
        "parse_filepath": f"{data_dir}/ES_v1_Spanish.xlsx",
        "style_data": style_data,
        "sheet_data": sheet_data,
        "language_code": "es",
    }

    viz = HaruGamesVisualizer(config)
    viz.create(
        intent_names=get_exportable_root_intents(sheet_data),
    )
