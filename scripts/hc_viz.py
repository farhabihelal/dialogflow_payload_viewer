import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../src"))


from dialogflow_payload_viewer.visualization import Visualizer

from datetime import datetime


class HCVisualizer(Visualizer):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def get_render_path(self, intent_name: str, language: str = "english"):
        path = os.path.join(
            os.path.abspath(self.config["render_path"]),
            datetime.now().strftime("%Y-%m-%d-%H:%M"),
            language.title(),
        )
        return path

    def get_exportable_root_intents(self) -> list:
        exportable_intentes = []
        gid_mapping = self.config["sheet_data"]["gid_mapping"]
        exportable_intentes = list(gid_mapping.keys())
        return exportable_intentes

    def get_url(self, node, language):
        intent_name = node.display_name
        sheet_data = self.config["sheet_data"]

        url = ""

        def get_sheet_mapping(name: str) -> tuple:
            """ """

            def get_sheet_name(name: str) -> str:
                return name.replace("topic-", "").strip().lower()

            gid = ""
            sheet_name = ""

            gid_mapping = self.config["sheet_data"]["gid_mapping"]
            sheet_name = get_sheet_name(name)
            gid = gid_mapping[name]

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
            "english": "https://docs.google.com/spreadsheets/d/1o022NBUApUV-mjQHImqDJvS3DovTv-kGIhIm04sqdDM/edit#",
            "spanish": "https://docs.google.com/spreadsheets/d/1o022NBUApUV-mjQHImqDJvS3DovTv-kGIhIm04sqdDM/edit#",
        },
        # Test
        # "base_url": "https://docs.google.com/spreadsheets/d/1kMeUTg8ewt-mtUago2ld7hG92vm1GBdT/edit#",
        "parameters": ["gid", "range"],
        "gid_mapping": {
            "topic-age": "849054916",
            "topic-band": "277372960",
            "topic-birthday": "2127363293",
            "topic-books": "1430542618",
            "topic-clothing": "981629445",
            "topic-fears": "8243799",
            "topic-food": "834720604",
            "game-would-you-rather": "129804009",
            "haru-games": "248553427",
            "topic-hobbies": "1489142799",
            "topic-hometown": "1878121241",
            "topic-intro": "1915275940",
            "topic-intro-short": "1344733719",
            "topic-language": "169041026",
            "topic-lemurs": "1537921349",
            "madlibs": "959426143",
            "topic-marriage": "1654776012",
            "topic-movies": "1182941535",
            "topic-music": "1709447283",
            "topic-names-origins": "105501088",
            "topic-olympics": "941832931",
            "topic-parents": "1641971905",
            "topic-pet": "2038502445",
            "topic-pet-new": "1065569868",
            "topic-profession": "2121474875",
            "topic-sports": "924832557",
            "topic-travel": "1309295636",
            "topic-travel-homecountry": "1388186892",
            "trivia-protocol": "128971995",
            "topic-weather": "1080780460",
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

    base_dir = os.path.abspath(f"{os.path.dirname(__file__)}/../")
    agent_dir = os.path.join(base_dir, ".temp/keys")
    data_dir = os.path.join(base_dir, "data")

    config = {
        "project_id": "haru-smalltalk-all-topics-gdga",
        "credential": f"{agent_dir}/haru-smalltalk-all-topics-lithin.json",
        "icons_path": f"{base_dir}/icons",
        "render_path": f"{base_dir}/renders/haru-chat",
        "sheet_data": sheet_data,
        "parse_filepath": f"{data_dir}/Haru-Chat.xlsx",
        "style_data": style_data,
    }

    viz = HCVisualizer(config)
    # viz.view()
