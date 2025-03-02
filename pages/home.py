from pathlib import Path

import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page, callback, Output, Input
from dash import html

from lib.constants import PAGE_TITLE_PREFIX
import dash_player as dp

register_page(
    __name__,
    "/",
    title=PAGE_TITLE_PREFIX + "Home",
)

directory = "docs"

# read all markdown files
md_file = Path("pages") / "home.md"

metadata, content = frontmatter.parse(md_file.read_text())


# directives = [Admonition(), BlockExec(), Divider(), Image(), Kwargs(), SC(), TOC()]
# parse = create_parser(directives)

layout = html.Div(
    [
        dmc.Container(
            size="lg",
            mt=30,
            children=dcc.Markdown(content)
        ),
        dp.DashPlayer(
            id="player",
            url="https://youtu.be/9Bcw_RmTQ2o?si=hsExmOB3436wZG6y",
            controls=True,
            width="80%",
            height="350px",
        ),

    ]
)

