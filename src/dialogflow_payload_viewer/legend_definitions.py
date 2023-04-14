import sys
import os

sys.path.append(os.path.abspath(f"{os.path.dirname(__file__)}/.."))


def get_legend_def(legend_data: dict, **kwargs):
    definition = ""

    definition += f"""
        <TABLE BGCOLOR="black" BORDER="4" CELLBORDER="0" CELLSPACING="0" CELLPADDING="20" STYLE="ROUNDED">
        <TR>
            <TD PORT="legend_title" COLSPAN="4" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""><FONT POINT-SIZE="" FACE=""><b>{legend_data.get('title', 'legend').upper()}</b></FONT></TD>
        </TR>
        """
    if len(legend_data.get("nodes", [])) > 0:
        definition += f"""
        <TR>
            <TD PORT="legend_node_title" COLSPAN="4" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""><FONT POINT-SIZE="" FACE=""><b>{'node types'.title()}</b></FONT></TD>
        </TR>
        """

    for i, node in enumerate(legend_data.get("nodes", [])):
        definition += f"""
        <TR>
            <TD PORT="legend_node_label_{i}" COLSPAN="3" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""><FONT POINT-SIZE="" FACE=""><b>{node['label'].title()}</b></FONT></TD>
            <TD PORT="legend_node_color_{i}" COLSPAN="1" STYLE="ROUNDED" BGCOLOR="{node['color']}" CELLPADDING="30" HREF=""></TD>
        </TR>
        """

    if len(legend_data.get("edges", [])) > 0:
        definition += f"""
        <TR>
            <TD PORT="legend_edge_title" COLSPAN="4" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""><FONT POINT-SIZE="" FACE=""><b>{'edge types'.title()}</b></FONT></TD>
        </TR>
        """

    for i, edge in enumerate(legend_data.get("edges", [])):
        definition += f"""
        <TR>
            <TD PORT="legend_edge_label_{i}" COLSPAN="3" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""><FONT POINT-SIZE="" FACE=""><b>{edge['label'].title()}</b></FONT></TD>
            <TD PORT="legend_edge_color_{i}" COLSPAN="1" STYLE="ROUNDED" BGCOLOR="" CELLPADDING="30" HREF=""></TD>
        </TR>
        """

    definition += f"""
        </TABLE>
        """

    return f"<{definition}>"


if __name__ == "__main__":
    legend_data = {
        "nodes": [
            {
                "label": "question node",
                "color": "",
            },
        ],
        "edges": [
            {
                "label": "impl",
                "color": "black",
                "style": "",
                "arrowsize": "2",
                "penwidth": "3.0",
            },
        ],
    }

    legend = get_legend_def(legend_data)

    print(legend)
