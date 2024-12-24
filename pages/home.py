from pathlib import Path

import frontmatter
import dash_mantine_components as dmc
from dash import dcc, register_page, callback, Output, Input
from dash import html

from lib.constants import PAGE_TITLE_PREFIX

register_page(
    __name__,
    "/",
    title=PAGE_TITLE_PREFIX + "Home",
)

directory = "docs"

file_path = Path(__file__).parent / "dash_leaflet-1.0.17.tar.gz"


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

        html.Center(html.Button("Download File", id="download-button")),
        dcc.Download(id="file-download"),
    ]
)


@callback(
    Output("file-download", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    # Return the absolute path to the file
    return dcc.send_file(file_path.resolve())