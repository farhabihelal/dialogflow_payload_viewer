import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from dialogflow_payload_gen.csv_parser_xl import CSVParserXL

from dialogflow import Dialogflow

import urllib

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

        for root_intent in root_intents:

            if root_intent.display_name not in [
                "topic-hometown",
                "topic-travel-homecountry",
            ]:
                continue

            graph = graphviz.Digraph(
                name=f"{root_intent.display_name}",
                directory=f"{self.config['render_path']}",
                # filename="",
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

            # graph.node('Root', style='filled')

            def create_edge(node):
                intent = node.intent_obj

                # graph.node(intent.display_name, **self._get_node_attrs(node))
                self.create_record_node(graph, node)

                if intent.action:
                    action = self._api.intents["display_name"].get(intent.action, None)
                    if action:
                        # graph.edge(intent.display_name, action._intent_obj.display_name, color='red', style='dotted')
                        graph.edge(
                            f"{intent.display_name}:action",
                            f"{action.display_name}",
                            color="red",
                            style="dotted",
                        )

                if node.parent:
                    parent = node.parent.intent_obj
                    # graph.node(f'name: {intent.name}', label=intent.display_name, style='filled', fillcolor='lightblue2')
                    graph.edge(f"{parent.display_name}", f"{intent.display_name}")
                else:
                    # graph.edge('Root', f'{intent.display_name}')
                    pass

                for child in node.children:
                    create_edge(child)

            create_edge(root_intent)

            graph.render(
                # filename=f"{intent.display_name}.gv",
                directory=self.config["render_path"],
                view=False,
                # format="pdf",
                # renderer="cairo",
                # engine="dot",
                # formatter="cairo",
                outfile=f"{root_intent.display_name}.pdf",
            )
            self._graphs.append(graph)

    def get_url(self, node):
        intent_name = node.display_name
        sheet_data = self.config["sheet_data"]

        url = ""

        def get_sheet_name(name: str):
            return name.replace("topic", "").replace("-", " ").strip().title()

        def get_response_indices(intents: list, intent_name: str) -> tuple:
            intent_rows = [
                x
                for x in intents
                if x[self._parser._header_map["intent"]] == intent_name
            ]
            start_idx = intents.index(next(iter(intent_rows)))
            end_idx = start_idx + len(intent_rows) - 1

            return start_idx, end_idx

        try:
            sheet_name = get_sheet_name(node.root.display_name)
            gid = sheet_data["gid_mapping"].get(sheet_name, "")
            intents = self._parser._data_sheets[sheet_name]
            start_idx, end_idx = get_response_indices(intents, intent_name)

            # url = f"{sheet_data['base_url']}gid={gid}&range={sheet_data['range_column']['start']}{start_idx}:{sheet_data['range_column']['end']}{end_idx}"
            url = f"{sheet_data['base_url']}gid={gid}&amp;range={sheet_data['range_column']['start']}{start_idx}:{sheet_data['range_column']['end']}{end_idx}"
        except Exception as e:
            pass

        # return urllib.parse.quote(url)
        return url

    def create_record_node(self, graph, node):

        record_def = ""

        node_color = "lightblue"

        if node.intent_obj.is_fallback:
            node_color = "pink"

        url = self.get_url(node)

        record_def += f"""
        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10" >
        <TR>
            <TD PORT="intent_name" COLSPAN="2" BGCOLOR="{node_color}" CELLPADDING="30" HREF="{url}"><FONT POINT-SIZE="32.0" FACE=""><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

        if node.intent_obj.action:
            record_def += f"""
        <TR>
            <TD ALIGN="CENTER"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
            <TD PORT="action" ALIGN="CENTER">{node.intent_obj.action}</TD>
        </TR>
        """

        # if len(node._intent_obj.parameters) > 0:
        #     record_def += f"""
        # <TR>
        #     <TD PORT="parameters" COLSPAN="2" ALIGN="CENTER"><IMG SRC="{self._icons_dir}/parameter-002-64x64.png"/></TD>
        # </TR>
        # """

        # for parameter in node._intent_obj.parameters:
        #     record_def += f"""
        # <TR>
        #     <TD>{parameter.display_name}</TD>
        #     <TD>{parameter.entity_type_display_name}</TD>
        # </TR>
        # """

        if node.has_text_messages:
            # record_def += f"""
            # <TR>
            #     <TD PORT="responses" COLSPAN="2" ALIGN="CENTER"><IMG SRC="{self.config["icons_path"]}/response-001-64x64.png"/></TD>
            # </TR>
            # """

            for i, responses in enumerate(node.text_messages):
                for j, paraphrase in enumerate(responses):
                    record_def += f"""
        <TR>
            <TD COLSPAN="2"><i>{paraphrase}</i></TD>
        </TR>
        """

        record_def += f"""
        </TABLE>
        """

        graph.node(node.display_name, f"<{record_def}>")

    def _get_node_attrs(self, node):
        result = {
            "color": "",
            "fillcolor": "0.25, 1.0, 0.7",
            "style": "filled",
        }

        return result

    def view(self):
        for graph in self._graphs:
            graph.view()


if __name__ == "__main__":

    sheet_data = {
        "base_url": "https://docs.google.com/spreadsheets/d/1o022NBUApUV-mjQHImqDJvS3DovTv-kGIhIm04sqdDM/edit#",
        "parameters": ["gid", "range"],
        "gid_mapping": {
            "Hometown": "1878121241",
            "Travel Homecountry": "1388186892",
        },
        "range_column": {
            "start": "F",
            "end": "K",
        },
    }

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        "project_id": "api-test-v99y",
        "credential": f"{agent_dir}/api-test.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders",
        "sheet_data": sheet_data,
        "parse_filepath": f"{data_dir}/haru-test.xlsx",
    }

    viz = Visualizer(config)
    viz.view()
