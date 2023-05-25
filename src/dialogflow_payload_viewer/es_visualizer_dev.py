import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils/src")
)


from dialogflow import Dialogflow, Intent
from node_definitions import get_node_def_advanced
from es_visualizer import ESVisualizer, get_exportable_root_intents


class ESVisualizerDev(ESVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def load(self, language_code: str = None):
        self._api.get_intents(
            language_code=language_code
            if language_code
            else self.config["language_code"]
        )
        self._api.generate_tree()

    def get_node_definition(self, node: Intent, **kwargs) -> str:
        # return get_node_def_basic(
        #     node, style_data=self.config["style_data"], url=self.get_url(node)
        # )
        return get_node_def_advanced(
            node, style_data=self.config["style_data"], url=self.get_url(node)
        )

    def get_url(self, node, *args, **kwargs):
        project_id = self.config["project_id"]
        intent_id = str(node.name).split("/")[-1]
        url = f"https://dialogflow.cloud.google.com/#/agent/{project_id}/editIntent/{intent_id}/"
        return url


if __name__ == "__main__":
    from styles import style_data
    from es_data import sheet_data

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    sheet_data = sheet_data["es2"]

    config = {
        # "credential": os.path.join(agent_dir, "es.json"),
        "credential": os.path.join(agent_dir, "es2.json"),
        # "credential": os.path.join(agent_dir, "haru-test.json"),
        "icons_path": os.path.join(base_dir, "icons"),
        "render_path": os.path.join(base_dir, "renders/ES-Dev"),
        "style_data": style_data,
        "sheet_data": sheet_data,
        "language_code": "en",
    }

    viz = ESVisualizerDev(config)
    viz.create(
        intent_names=get_exportable_root_intents(sheet_data),
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
