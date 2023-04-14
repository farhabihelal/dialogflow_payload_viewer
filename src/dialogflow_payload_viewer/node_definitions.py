import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/.."))

from dialogflow import Intent

import html


def get_node_def_basic(node: Intent, **kwargs):
    definition = ""

    custom_payload: dict = node.custom_payload
    node_type = custom_payload.get("node_type", "")

    style_data = (
        kwargs["style_data"]["fallback"]
        if node_type == "FallbackNode"
        else kwargs["style_data"]["disabled"]
        if node_type == "DisabledNode" or node.intent_obj.priority < 0
        else kwargs["style_data"]["default"]
    )

    definition += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="intent_name" COLSPAN="2" STYLE="ROUNDED" BGCOLOR="{style_data['intent-name']['color']}" CELLPADDING="30" HREF="{kwargs.get('url', '')}"><FONT POINT-SIZE="{style_data['intent-name']['font-size']}" FACE="{style_data['intent-name']['font']}"><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

    # if node.intent_obj.action:
    #     definition += f"""
    # <TR>
    #     <TD BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
    #     <TD PORT="action" BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['action']['font-size']}" FACE="{style_data['action']['font']}">{node.intent_obj.action}</FONT></TD>
    # </TR>
    # """

    if node.has_text_messages:
        for i, responses in enumerate(node.text_messages):
            if i > 0:
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="black" CELLPADDING="5" STYLE="ROUNDED"></TD>
        </TR>
        """
            for j, paraphrase in enumerate(responses):
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="{style_data['messages']['color']}" CELLPADDING="20" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['messages']['font-size']}" FACE="{style_data['messages']['font']}"><i>{html.escape(paraphrase)}</i></FONT></TD>
        </TR>
        """

    definition += f"""
        </TABLE>
        """

    return f"<{definition}>"


def get_node_def_advanced(node: Intent, **kwargs):
    definition = ""

    custom_payload: dict = node.custom_payload
    node_type = custom_payload.get("node_type", "")
    # local_transformer_classifier = custom_payload.get("node_type", "")

    style_data = (
        kwargs["style_data"]["fallback"]
        if node_type == "FallbackNode"
        else kwargs["style_data"]["question"]
        if node_type == "QuestionNode"
        else kwargs["style_data"]["answer"]
        if node_type == "AnswerNode"
        else kwargs["style_data"]["answer-question"]
        if node_type == "AnswerQuestionNode"
        else kwargs["style_data"]["disabled"]
        if node_type == "DisabledNode"
        # else kwargs["style_data"]["repeat"]
        # if node_type == "RepeatNode"
        else kwargs["style_data"]["default"]
    )

    definition += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="intent_name" COLSPAN="2" STYLE="ROUNDED" BGCOLOR="{style_data['intent-name']['color']}" CELLPADDING="30" HREF="{kwargs.get('url', '')}"><FONT POINT-SIZE="{style_data['intent-name']['font-size']}" FACE="{style_data['intent-name']['font']}"><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

    # if node.intent_obj.action:
    #     definition += f"""
    # <TR>
    #     <TD BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
    #     <TD PORT="action" BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['action']['font-size']}" FACE="{style_data['action']['font']}">{node.intent_obj.action}</FONT></TD>
    # </TR>
    # """

    if node.has_text_messages:
        for i, responses in enumerate(node.text_messages):
            if i > 0:
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="black" CELLPADDING="5" STYLE="ROUNDED"></TD>
        </TR>
        """
            for j, paraphrase in enumerate(responses):
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="{style_data['messages']['color']}" CELLPADDING="20" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['messages']['font-size']}" FACE="{style_data['messages']['font']}"><i>{html.escape(paraphrase)}</i></FONT></TD>
        </TR>
        """

    definition += f"""
        </TABLE>
        """

    return f"<{definition}>"


def get_node_def_issue(node: Intent, **kwargs):
    definition = ""

    style_data = (
        kwargs["style_data"]["issue"]
        if kwargs.get("has_issue", False)
        else kwargs["style_data"]["default"]
    )

    definition += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="intent_name" COLSPAN="2" STYLE="ROUNDED" BGCOLOR="{style_data['intent-name']['color']}" CELLPADDING="30" HREF="{kwargs.get('url', '')}"><FONT POINT-SIZE="{style_data['intent-name']['font-size']}" FACE="{style_data['intent-name']['font']}"><b>{node.display_name}</b></FONT></TD>
        </TR>
        """

    # if node.intent_obj.action:
    #     definition += f"""
    # <TR>
    #     <TD BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><IMG SRC="{self.config["icons_path"]}/action-004-64x64.png"/></TD>
    #     <TD PORT="action" BGCOLOR="{style_data['action']['color']}" ALIGN="CENTER" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['action']['font-size']}" FACE="{style_data['action']['font']}">{node.intent_obj.action}</FONT></TD>
    # </TR>
    # """

    if node.has_text_messages:
        for i, responses in enumerate(node.text_messages):
            if i > 0:
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="black" CELLPADDING="5" STYLE="ROUNDED"></TD>
        </TR>
        """
            for j, paraphrase in enumerate(responses):
                definition += f"""
        <TR>
            <TD COLSPAN="2" BGCOLOR="{style_data['messages']['color']}" CELLPADDING="20" STYLE="ROUNDED"><FONT POINT-SIZE="{style_data['messages']['font-size']}" FACE="{style_data['messages']['font']}"><i>{html.escape(paraphrase)}</i></FONT></TD>
        </TR>
        """

    definition += f"""
        </TABLE>
        """

    return f"<{definition}>"
