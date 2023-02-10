import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

import webbrowser
from dialogflow import Dialogflow, Intent


from datetime import datetime


class IntentUI:
    def __init__(self, config: dict) -> None:
        """Constructor

        Args:
            config (dict): Configuration
        """
        self.configure()

        self._api = Dialogflow(config)

        pass

    def open_in_brower(self, intent: Intent):
        agent_name = ""
        intent_uuid = ""
        url = f"https://dialogflow.cloud.google.com/#/agent/{agent_name}/editIntent/{intent_uuid}/"

        webbrowser.open_new_tab(url)

    def configure(self, config: dict):
        self.config = config


if __name__ == "__main__":
    pass
