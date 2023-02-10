import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from dialogflow import Dialogflow, Intent
from graphviz import Digraph


class BaseVisualizer:
    def __init__(self, config: dict) -> None:
        self.configure(config)
        self._api = Dialogflow(self.config)

        self._graphs = []

    def configure(self, config: dict):
        self.config = config

    def load(self):
        """ """
        self._api.get_intents()
        self._api.generate_tree()

    def create(self, intent_names: list = None, blacklisted_intent_names: list = []):
        """
        Intent Filtering Logic

        intent_names > blacklisted_intent_names

        ALLOWED     : If intent_name is found in intent_names. Does not matter blacklisted_intent_names.
        FILTERED    : Only if intent_name is found in blacklisted_intent_names.
        """
        self.load()

        intents = [
            self._api.intents["display_name"][x]
            for x in self.filter(
                list(self._api.intents["display_name"].keys()),
                intent_names,
                blacklisted_intent_names,
            )
        ]
        self.create_graph(intents=intents)

    def filter(self, input: list, whitelist: list, blacklist: list):
        return [
            value
            for value in input
            if (whitelist is not None and value in whitelist)
            or (whitelist is not None and value in whitelist and value not in blacklist)
            or (whitelist is None and value not in blacklist)
        ]

    def create_graph(self, intents: list):
        """ """
        for intent in intents:
            intent: Intent
            graph = self.get_graph(
                name=f"{intent.display_name}",
                directory=self.get_render_path(intent.display_name),
                filename=f"{intent.display_name}.gv",
                format="pdf",
            )

            self.create_edge(graph, intent)

            graph.render(
                # filename=f"{intent.display_name}.gv",
                # directory=f"{os.path.abspath(self.config['render_path'])}/{datetime.now().strftime('%Y-%m-%d-%H:%M')}",
                view=False,
                # format="pdf",
                # renderer="cairo",
                # engine="dot",
                # formatter="cairo",
                outfile=os.path.join(
                    self.get_render_path(intent.display_name),
                    f"{intent.display_name}.pdf",
                ),
            )
            self._graphs.append(graph)

    def get_graph(
        self, name=None, directory=None, filename=None, format=None
    ) -> Digraph:
        """ """
        graph = Digraph(
            name=name,
            directory=directory,
            filename=filename,
            edge_attr={},
            graph_attr={},
            node_attr={
                "shape": "plaintext",
            },
            format=format,
            engine="dot",
            formatter="cairo",
            renderer="cairo",
        )
        return graph

    def create_edge(self, graph: Digraph, node: Intent):
        """ """
        intent = node.intent_obj

        graph.node(node.display_name, self.get_node_definition(node))

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
            self.create_edge(graph, child)

    def get_render_path(self, node: Intent):
        path = os.path.abspath(self.config["render_path"])
        return path

    def get_node_definition(self, node: Intent):
        definition = ""

        style_data = (
            self.config["style_data"]["fallback"]
            if node.intent_obj.is_fallback
            else self.config["style_data"]["default"]
        )

        definition += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="intent_name" COLSPAN="2" STYLE="ROUNDED" BGCOLOR="{style_data['intent-name']['color']}" CELLPADDING="30" HREF=""><FONT POINT-SIZE="{style_data['intent-name']['font-size']}" FACE="{style_data['intent-name']['font']}"><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

        # if node.intent_obj.action:
        #     definition += f"""
        # <TR>
        #     <TD BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
        #     <TD PORT="action" BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['action']['font-size']}" FACE="{style_data['action']['font']}">{node.intent_obj.action}</FONT></TD>
        # </TR>
        # """

        if node.has_text_messages:
            for i, responses in enumerate(node.text_messages):
                if i > 0:
                    definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="black" CELLPADDING="5" STYLE="ROUNDED"></TD>
        </TR>
        """
                for j, paraphrase in enumerate(responses):
                    definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="{style_data['messages']['color']}" CELLPADDING="20" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['messages']['font-size']}" FACE="{style_data['messages']['font']}"><i>{paraphrase}</i></FONT></TD>
        </TR>
        """

        definition += f"""
        </TABLE>
        """

        return f"<{definition}>"

    def view(self):
        for graph in self._graphs:
            graph.view()


if __name__ == "__main__":
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
        "style_data": style_data,
    }

    viz = BaseVisualizer(config)
    viz.create(
        intent_names=["topic-day-one-session-one-age"],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
