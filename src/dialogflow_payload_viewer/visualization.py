import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/../dialogflow-api/src/"))

from datetime import datetime

from dialogflow import Dialogflow

import graphviz


class Visualizer:
    def __init__(self, config: dict) -> None:

        self.configure(config)

        self._api = Dialogflow(self.config)

        self._graphs = []

        self.create()

    def configure(self, config: dict):
        self.config = config

    # def create(self):

    #     for key in self._intents:
    #         intent = self._intents[key]._intent_obj

    #         if not intent.parent_followup_intent_name:
    #             self._graph.edge('Root', intent.display_name)
    #         else:
    #             parent = self._intents[intent.parent_followup_intent_name]._intent_obj
    #             self._graph.edge(parent.display_name, intent.display_name)

    # def create(self):

    #     for branch in self._branches:

    #         graph = graphviz.Digraph(
    #             f"{branch._intent_obj.display_name}",
    #             node_attr={"color": "lightblue2", "style": "filled"},
    #             format="png",
    #             engine="dot",
    #             formatter="cairo",
    #             renderer="cairo",
    #         )

    #         def create_edge(node):
    #             intent = node._intent_obj

    #             graph.node(intent.display_name, **self._get_node_attrs(node))

    #             if intent.action:
    #                 action = self._intents_display.get(intent.action, None)
    #                 if action:
    #                     graph.edge(
    #                         intent.display_name,
    #                         action._intent_obj.display_name,
    #                         color="red",
    #                         style="dotted",
    #                     )

    #             if node._parent:
    #                 parent = node._parent._intent_obj
    #                 # graph.node(f'name: {intent.name}', label=intent.display_name, style='filled', fillcolor='lightblue2')
    #                 graph.edge(parent.display_name, intent.display_name)
    #             else:
    #                 graph.edge("Root", intent.display_name)

    #             for child in node._children:
    #                 create_edge(child)

    #         create_edge(branch)

    #         graph.view()
    #         self._graphs.append(graph)

    def create(self):
        """ """
        self._api.get_intents()

        self.create_record()

    def create_record(self):
        """ """
        root_intents = self._api.get_root_intents()

        for intent in self.root_intents:

            graph = graphviz.Digraph(
                f"{intent.display_name}",
                node_attr={
                    "shape": "plaintext",
                },
                format="pdf",
                engine="dot",
                formatter="cairo",
                renderer="cairo",
            )

            # graph.node('Root', style='filled')

            def create_edge(node):
                intent = node._intent_obj

                # graph.node(intent.display_name, **self._get_node_attrs(node))
                self.create_record_node(graph, node)

                if intent.action:
                    action = self._intents_display.get(intent.action, None)
                    if action:
                        # graph.edge(intent.display_name, action._intent_obj.display_name, color='red', style='dotted')
                        graph.edge(
                            f"{intent.display_name}:action",
                            f"{action._intent_obj.display_name}",
                            color="red",
                            style="dotted",
                        )

                if node._parent:
                    parent = node._parent._intent_obj
                    # graph.node(f'name: {intent.name}', label=intent.display_name, style='filled', fillcolor='lightblue2')
                    graph.edge(f"{parent.display_name}", f"{intent.display_name}")
                else:
                    # graph.edge('Root', f'{intent.display_name}')
                    pass

                for child in node._children:
                    create_edge(child)

            create_edge(intent)

            graph.render(
                filename=f"{intent.display_name}.gv",
                directory=self.config["render_dir"],
                view=False,
                format="pdf",
                renderer="cairo",
                engine="dot",
                formatter="cairo",
                outfile=f"{intent.display_name}.pdf",
            )
            self._graphs.append(graph)

    def create_record_node(self, graph, node):

        record_def = ""

        node_color = "lightblue"

        if node._intent_obj.is_fallback:
            node_color = "pink"

        record_def += f"""
        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" CELLPADDING="10" >
        <TR>
            <TD PORT="intent_name" COLSPAN="2" BGCOLOR="{node_color}" CELLPADDING="30"><FONT POINT-SIZE="32.0" FACE=""><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

        # if len(node.training_phrases) > 0:

        #     color = "0.25, 1.0, 0.7"

        #     if len(node.training_phrases) < 2:
        #         color = "0.0, 1.0, 0.7"
        #     elif len(node.training_phrases) < 7:
        #         color = "0.1, 1.0, 0.7"

        #     record_def += f"""
        # <TR>
        #     <TD ALIGN="CENTER"><IMG SRC="{self._icons_dir}/ml-001-64x64.png"/></TD>
        #     <TD BGCOLOR="{color}"><FONT POINT-SIZE="20.0"><b>{len(node.training_phrases)}</b></FONT> phrases</TD>
        # </TR>
        # """

        #     for i, phrase in enumerate(node.training_phrases):
        #         if i > 2:
        #             break
        #         record_def += f"""
        # <TR>
        #     <TD COLSPAN="2"><i>{phrase}</i></TD>
        # </TR>
        # """

        if node.intent_obj.action:
            record_def += f"""
        <TR>
            <TD ALIGN="CENTER"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
            <TD PORT="action" ALIGN="CENTER">{node.intent_obj.action}</TD>
        </TR>
        """

        # if len(node._intent_obj.parameters) > 0:
        #     record_def += f"""
        # <TR>
        #     <TD PORT="parameters" COLSPAN="2" ALIGN="CENTER"><IMG SRC="{self._icons_dir}/parameter-002-64x64.png"/></TD>
        # </TR>
        # """

        # for parameter in node._intent_obj.parameters:
        #     record_def += f"""
        # <TR>
        #     <TD>{parameter.display_name}</TD>
        #     <TD>{parameter.entity_type_display_name}</TD>
        # </TR>
        # """

        if node.has_messages:
            record_def += f"""
        <TR>
            <TD PORT="responses" COLSPAN="2" ALIGN="CENTER"><IMG SRC="{self.config["icons_path"]}/response-001-64x64.png"/></TD>
        </TR>
        """

            for message_list in node.messages:
                for i, message in enumerate(message_list):
                    # if i > 0:
                    #     break
                    record_def += f"""
        <TR>
            <TD COLSPAN="2"><i>{message}</i></TD>
        </TR>
        """

        record_def += f"""
        </TABLE>
        """

        graph.node(node.intent_obj.display_name, f"<{record_def}>")

    def _get_node_attrs(self, node):
        result = {
            "color": "",
            "fillcolor": "0.25, 1.0, 0.7",
            "style": "filled",
        }

        # if len(node.traning_phrases) < 2:
        #     result["fillcolor"] = "0.0, 1.0, 0.7"
        # elif len(node.traning_phrases) < 7:
        #     result["fillcolor"] = "0.1, 1.0, 0.7"

        return result

    def view(self):
        for graph in self._graphs:
            graph.view()


if __name__ == "__main__":
    config = {
        "project_id": "",
        "credential": "",
        "icons_path": "",
        "render_dir": "",
    }

    viz = Visualizer(config)
    viz.view()
