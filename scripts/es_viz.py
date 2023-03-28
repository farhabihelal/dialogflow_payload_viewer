import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../src"))

from datetime import datetime
from dialogflow_payload_viewer.visualization import Visualizer


class ESVisualizer(Visualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

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

    def get_exportable_root_intents(self) -> list:
        exportable_intentes = []

        gid_mapping = self.config["sheet_data"]["gid_mapping"]
        for day in gid_mapping:
            for session in gid_mapping[day]:
                intents = gid_mapping[day][session]["intents"]
                exportable_intentes.extend(intents)

        return exportable_intentes

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


if __name__ == "__main__":

    sheet_data = {
        "languages": ["english", "spanish"],
        # Actual
        "base_url": {
            # v1
            # "english": "https://docs.google.com/spreadsheets/d/16jQ8q7M72dBdkxpcIKPXT1nRQbmD4wibZIQRgN_84X8/edit#",
            # v2
            "english": "https://docs.google.com/spreadsheets/d/1EDO4AebEr8kygh9Bxt_uO0m2jJ-0wITpolYjtKBjo04/edit#",
            "spanish": "https://docs.google.com/spreadsheets/d/1-VE3Rw25G_Z3DKpYPCcg-jmix3oUf2JdVMDLR6FJhOs/edit#",
            # Test
            # "english": "https://docs.google.com/spreadsheets/d/1QDuaijqR4I7CFws_kzww6JZS08QAde6i/edit#",
        },
        "parameters": ["gid", "range"],
        "gid_mapping": {
            "1": {
                "1": {
                    "gid": "1163585192",
                    "intents": [
                        "topic-intro",
                        "topic-day-one-session-one-names-origins",
                        "topic-day-one-session-one-transition-age",
                        "topic-day-one-session-one-age",
                    ],
                },
                "2": {
                    "gid": "919985165",
                    "intents": [
                        "topic-day-one-session-two-intro",
                        "topic-travel-homecountry",
                        "topic-day-one-session-two-transition",
                        "topic-hometown",
                        "topic-day-one-session-two-outro",
                    ],
                },
            },
            "2": {
                "1": {
                    "gid": "743627153",
                    "intents": [
                        "topic-day-two-session-one-intro",
                        "topic-day-two-family",
                        "topic-day-two-session-one-transition",
                        "topic-day-two-parents",
                        "topic-day-two-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "2061915944",
                    "intents": [
                        "topic-day-two-session-two-intro",
                        "topic-pet-new",
                        "topic-day-two-session-two-transition",
                        "topic-lemurs",
                        "topic-day-two-session-two-end",
                    ],
                },
            },
            "3": {
                "1": {
                    "gid": "81336119",
                    "intents": [
                        "topic-day-three-session-one-intro",
                        "topic-day-three-food",
                        "topic-day-three-session-one-transition",
                        "topic-birthday",
                        "topic-day-three-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "1627598687",
                    "intents": [
                        "topic-day-three-session-two-intro",
                        "topic-sports",
                        "topic-day-three-session-two-transition",
                        "topic-day-three-hobbies",
                        "topic-day-three-session-two-outro",
                    ],
                },
            },
            "4": {
                "1": {
                    "gid": "592896325",
                    "intents": [
                        "topic-day-four-session-one-intro",
                        "topic-day-four-school",
                        "topic-day-four-session-one-transition",
                        "topic-day-four-friends",
                        "topic-day-four-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "804812225",
                    "intents": [
                        "topic-day-four-session-two-intro",
                        "topic-language",
                        "topic-day-four-session-two-transition",
                        "topic-music",
                        "topic-day-four-session-two-outro",
                    ],
                },
            },
            "5": {
                "1": {
                    "gid": "1381156119",
                    "intents": [
                        "topic-day-five-session-one-intro",
                        "topic-day-five-weather",
                        "topic-day-five-session-one-transition",
                        "topic-day-five-clothing",
                        "topic-day-five-session-one-outro",
                    ],
                },
                "2": {
                    "gid": "148830916",
                    "intents": [
                        "topic-day-five-session-two-intro",
                        "topic-day-five-travel",
                        "topic-day-five-session-two-transition",
                        "topic-olympics",
                        "topic-day-five-session-two-outro",
                    ],
                },
                "3": {
                    "gid": "2048883617",
                    "intents": [
                        "topic-day-five-session-three-intro",
                        "topic-day-five-session-three-poem",
                        "topic-day-five-session-three-outro",
                    ],
                },
            },
        },
        "range_column": {
            "start": "B",
            "end": "K",
        },
    }

    from dialogflow_payload_viewer.styles import es_style_data

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        "credential": f"{agent_dir}/es.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders/es-demo",
        "sheet_data": sheet_data,
        "parse_filepath": f"{data_dir}/ES_merged.xlsx",
        "style_data": es_style_data,
    }

    viz = ESVisualizer(config)
    # viz.view()
