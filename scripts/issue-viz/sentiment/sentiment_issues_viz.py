import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../../../src"))

from datetime import datetime
from dialogflow_payload_viewer.issue_visualizer import IssueVisualizer
from dialogflow import Dialogflow
from intent import Intent


def load_api(api: Dialogflow):
    api.get_intents()
    api.generate_tree()


def get_issued_intents(api: Dialogflow, root_intent_names: list):
    issued_intents = set()

    fallbacks_to_check = []
    dummies_to_check = []

    for root_intent_name in root_intent_names:
        root_intent: Intent = api.intents["display_name"][root_intent_name]

        for intent in root_intent.all_children_bfs:
            intent: Intent
            if (
                intent.is_fallback
                or hasattr(intent.custom_payload, "node_type")
                and intent.custom_payload.get["node_type"] == "FallbackNode"
            ):
                for child in intent.children:
                    child: Intent
                    if "dummy" in child.display_name:
                        fallbacks_to_check.append(intent)
                        # dummies_to_check.append(child)
                        # if intent.action != child.display_name:
                        #     issued_intents.add(intent)
                        break

    for fallback in fallbacks_to_check:
        fallback: Intent
        if not "sentiment_classification_override" in fallback.custom_payload:
            issued_intents.add(fallback)

    return list(issued_intents)


if __name__ == "__main__":
    from dialogflow_payload_viewer.styles import issue_style_data

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../../../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        # "credential": f"{agent_dir}/child-in-hospital.json",
        # "credential": f"{agent_dir}/es.json",
        "credential": f"{agent_dir}/haru-test.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders/Sent-Issues",
        "style_data": issue_style_data,
        "language_code": en-us,
        "intents": [],
        "issued_intents": [],
    }

    viz = IssueVisualizer(config)
    api = viz._api
    load_api(api)
    intent_names = [
        "topic-day-two-parents",
        "topic-day-two-family",
        "topic-pet-new",
        "topic-lemurs",
    ]
    viz.create(
        intent_names=intent_names,
        issued_intent_names=[
            x.display_name
            for x in get_issued_intents(api=api, root_intent_names=intent_names)
        ],
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
