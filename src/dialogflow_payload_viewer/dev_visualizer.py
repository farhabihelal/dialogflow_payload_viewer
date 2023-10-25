import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from base_visualizer import BaseVisualizer
from dialogflow import Dialogflow, Intent
from graphviz import Digraph

from node_definitions import get_node_def_advanced

import google.cloud.dialogflow_v2 as dialogflow_v2


class DevVisualizer(BaseVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        # return get_node_def_basic(
        #     node, style_data=self.config["style_data"], url=self.get_url(node)
        # )
        return get_node_def_advanced(
            node, style_data=self.config["style_data"], url=self.get_url(node)
        )

    def get_url(self, node: Intent):
        intent_id = str(node.name).split("/")[-1]
        url = f"https://dialogflow.cloud.google.com/#/agent/{self.config['project_id']}/editIntent/{intent_id}/"
        return url

    def get_render_path(self, node: Intent):
        path = os.path.abspath(self.config["render_path"])
        return path


if __name__ == "__main__":
    from styles import style_data

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        # "credential": os.path.join(agent_dir, "haru-magic.json"),
        "credential": os.path.join(agent_dir, "tiny-tiny-habits-rvuq.json"),
        "icons_path": os.path.join(base_dir, "icons"),
        "render_path": os.path.join(base_dir, "renders", "tiny_habits"),
        "style_data": style_data,
    }

    viz = DevVisualizer(config)
    viz.create(
        intent_names=[
            "tiny-tiny-intro",
            "topic-tiny-habits2-anchor",
            "topic-tiny-habits2-aspiration",
            "topic-tiny-habits2-celebration",
            "topic-tiny-habits2-end",
            "topic-tiny-habits2-intro",
            "topic-tiny-habits2-scaling",
            "topic-tiny-habits2-test-anchor",
            "topic-tiny-habits2-test-aspiration",
            "topic-tiny-habits2-test-celebration",
            "topic-tiny-habits2-test-end",
            "topic-tiny-habits2-test-scaling",
            "topic-tiny-tiny-elements",
            "would-you-rather-protocol",
            "topic-tiny-tiny-end",
            "topic-tiny-tiny-idea",
            "topic-tiny-tiny-motivation",
            "topic-tiny-tiny-scaling",
            "topic-tiny-tiny-secret",
        ],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
