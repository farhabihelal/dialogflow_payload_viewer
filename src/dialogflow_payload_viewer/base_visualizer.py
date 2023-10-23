import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from dialogflow import Dialogflow, Intent
from graphviz import Digraph

from node_definitions import get_node_def_basic
from legend_definitions import get_legend_def


class BaseVisualizer:
    def __init__(self, config: dict) -> None:
        self.configure(config)
        self._api = Dialogflow(self.config)

        self._graphs = []

    def configure(self, config: dict):
        self.config = config

    def load(self, language_code="en-us"):
        """ """
        self._api.get_intents(language_code=language_code)
        self._api.generate_tree()

    def create(
        self,
        intent_names: list = None,
        blacklisted_intent_names: list = [],
        language_code=None,
        **kwargs,
    ):
        """
        Intent Filtering Logic

        intent_names > blacklisted_intent_names

        ALLOWED     : If intent_name is found in intent_names. Does not matter blacklisted_intent_names.
        FILTERED    : Only if intent_name is found in blacklisted_intent_names.
        """
        self.load(language_code=language_code)

        intent_names = (
            intent_names
            if intent_names
            else [x.display_name for x in self._api.get_root_intents()]
        )

        intents = [
            self._api.intents["display_name"][x]
            for x in self.filter(
                list(self._api.intents["display_name"].keys()),
                intent_names,
                blacklisted_intent_names,
            )
        ]
        self.create_graph(intents=intents, **kwargs)

    def filter(self, input: list, whitelist: list, blacklist: list):
        return [
            value
            for value in input
            if (whitelist is not None and value in whitelist)
            or (whitelist is not None and value in whitelist and value not in blacklist)
            or (whitelist is None and value not in blacklist)
        ]

    def create_graph(self, intents: list, **kwargs):
        """ """
        for intent in intents:
            intent: Intent
            graph = self.get_graph(
                name=f"{intent.display_name}",
                directory=os.path.join(
                    self.get_render_path(intent.display_name), "DOT"
                ),
                filename=f"{intent.display_name}.gv",
                format="pdf",
            )

            self.create_edge(graph, intent, **kwargs)
            # self.create_legend(graph, self.config.get("legend_data", {}))

            graph.render(
                # filename=f"{intent.display_name}.gv",
                # directory=f"{os.path.abspath(self.config['render_path'])}/{datetime.now().strftime('%Y-%m-%d-%H:%M')}",
                view=False,
                # format="pdf",
                # renderer="cairo",
                # engine="neato",
                # formatter="cairo",
                outfile=os.path.join(
                    self.get_render_path(intent.display_name),
                    f"{intent.display_name}.pdf",
                ),
            )
            self._graphs.append(graph)

    def get_graph_legend_definitions(self, legend_data: dict):
        return get_legend_def(legend_data)

    def create_legend(self, graph: Digraph, legend_data: dict) -> Digraph:
        graph.node(
            "legend", self.get_graph_legend_definitions(legend_data), pos="20,20!"
        )

        def create_legend_edge(graph: Digraph, legend_data: dict):
            edges = legend_data.get("edges", [])

            for i, edge in enumerate(edges):
                graph.edge(
                    f"legend_edge_label_{i}",
                    f"legend_edge_color_{i}",
                    color=f"{edge['color']}",
                    style=f"{edge['style']}",
                    arrowsize=f"{edge['arrowsize']}",
                    penwidth=f"{edge['penwidth']}",
                    # **edge,
                )

        create_legend_edge(graph, legend_data)

        return graph

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

    def create_edge(self, graph: Digraph, node: Intent, **kwargs):
        """ """
        intent = node.intent_obj

        graph.node(
            node.display_name,
            self.get_node_definition(node, **kwargs),
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

    def get_render_path(self, node: Intent):
        path = os.path.abspath(self.config["render_path"])
        return path

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        return get_node_def_basic(node, style_data=self.config["style_data"], **kwargs)

    def view(self):
        for graph in self._graphs:
            graph.view()


if __name__ == "__main__":
    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    from styles import style_data

    legend_data = {
        "nodes": [
            {
                "label": "question node",
                "color": "red",
            },
        ],
        "edges": [
            {
                "label": "impl",
                "color": "black",
                "style": "",
                "arrowsize": "2",
                "penwidth": "3.0",
            },
        ],
    }

    config = {
        "credential": f"{agent_dir}/tiny-tiny-habits-rvuq.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders",
        "style_data": style_data,
        "legend_data": legend_data,
    }

    viz = BaseVisualizer(config)
    viz.create(
        intent_names=["tiny-tiny-intro"],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
