import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))
sys.path.append(
    os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow_payload_utils")
)

from es_visualizer import ESVisualizer, get_exportable_root_intents


class ESVisualizerDev(ESVisualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_url(self, node, *args, **kwargs):
        project_id = self.config["project_id"]
        intent_id = str(node.name).split("/")[-1]
        url = f"https://dialogflow.cloud.google.com/#/agent/{project_id}/editIntent/{intent_id}/"
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
        # "project_id": "empathetic-stimulator-owp9",
        "credential": f"{agent_dir}/es.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders",
        "parse_filepath": f"{data_dir}/ES_manual_merge.xlsx",
        "style_data": style_data,
        "sheet_data": sheet_data,
    }

    viz = ESVisualizerDev(config)
    viz.create(
        intent_names=get_exportable_root_intents(sheet_data),
        # blacklisted_intent_names=["knew-baseball-fact-no"],
    )
    # viz.view()
