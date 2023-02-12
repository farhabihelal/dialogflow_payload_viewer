import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from base_visualizer import BaseVisualizer
from dialogflow import Dialogflow, Intent
from graphviz import Digraph

from node_definitions import get_node_def_basic

import google.cloud.dialogflow_v2 as dialogflow_v2


class DevVisualizer(BaseVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        return get_node_def_basic(
            node, style_data=self.config["style_data"], url=self.get_url(node)
        )

    def get_url(self, node: Intent):
        intent_id = str(node.name).split("/")[-1]
        url = f"https://dialogflow.cloud.google.com/#/agent/{self.config['project_id']}/editIntent/{intent_id}/"
        return url

    def get_render_path(self, node: Intent):
        path = os.path.abspath(self.config["render_path"])
        return path

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

    viz = DevVisualizer(config)
    viz.create(
        intent_names=["topic-day-one-session-one-age"],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
