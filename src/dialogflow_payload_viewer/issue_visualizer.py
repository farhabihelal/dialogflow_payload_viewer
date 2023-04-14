import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from dev_visualizer import DevVisualizer
from dialogflow import Dialogflow, Intent
from graphviz import Digraph

from node_definitions import get_node_def_issue

import google.cloud.dialogflow_v2 as dialogflow_v2


class IssueVisualizer(DevVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        # return get_node_def_basic(
        #     node, style_data=self.config["style_data"], url=self.get_url(node)
        # )
        return get_node_def_issue(
            node, style_data=self.config["style_data"], url=self.get_url(node), **kwargs
        )

    def get_url(self, node: Intent):
        intent_id = str(node.name).split("/")[-1]
        url = f"https://dialogflow.cloud.google.com/#/agent/{self.config['project_id']}/editIntent/{intent_id}/"
        return url

    def get_render_path(self, node: Intent):
        path = os.path.join(
            os.path.abspath(self.config["render_path"]),
            os.path.splitext(os.path.basename(self.config["credential"]))[0],
        )
        return path

    def create_graph(self, intents: list, **kwargs):
        """ """
        issued_intent_names = kwargs["issued_intent_names"]

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

            self.create_edge(
                graph,
                intent,
                has_issue=True if intent.display_name in issued_intent_names else False,
            )

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


if __name__ == "__main__":
    from styles import issue_style_data

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        # "credential": f"{agent_dir}/haru-chat-games.json",
        "credential": f"{agent_dir}/haru-test.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders/issues-viz",
        "style_data": issue_style_data,
    }

    viz = IssueVisualizer(config)
    viz.create(
        intent_names=[],
        issued_intent_names=[],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
