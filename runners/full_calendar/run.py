import sys
from pathlib import Path

from dash import Dash, Input, Output, dcc, html, _dash_renderer
import dash_mantine_components as dmc

# Ensure the repo root is on sys.path so docs/* modules import cleanly when this
# runner is executed from its own directory.
CURRENT_FILE = Path(__file__).resolve()
RUNNER_DIR = CURRENT_FILE.parent
REPO_ROOT = RUNNER_DIR.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Use the shared assets directory (dark theme CSS, icons, etc.).
ASSETS_PATH = REPO_ROOT / "assets"

# Set React 18 so dash-mantine-components loads correctly
_dash_renderer._set_react_version("18.2.0")

stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
    "https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.css",
    "https://use.fontawesome.com/releases/v6.2.1/css/all.css",
]

scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/ru.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/fr.min.js",
    "https://unpkg.com/hotkeys-js/dist/hotkeys.min.js",
]

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_scripts=scripts,
    external_stylesheets=stylesheets + dmc.styles.ALL,
    assets_folder=str(ASSETS_PATH),
    title="Dash FullCalendar Showcase",
)

# Import the interactive examples after the Dash app exists so callbacks attach cleanly.
from docs.full_calendar_component import (  # noqa: E402
    api_example,
    extra_fields,
    header_toolbar,
    introduction,
    section_renders,
)

HOME_MD = (REPO_ROOT / "pages/home.md").read_text()


def render_home():
    return dmc.Container(
        [
            dmc.Title("Pip Install Python Components", order=2),
            dmc.Space(h=10),
            dcc.Markdown(HOME_MD),
        ],
        size="lg",
        py="xl",
    )


def render_full_calendar_docs():
    return dmc.Container(
        [
            dmc.Title("Dash FullCalendar Showcase", order=2),
            dmc.Text(
                "Minimal runner containing the home page and the Dash FullCalendar examples only.",
                c="dimmed",
            ),
            dmc.Divider(label="Interactive Builder"),
            introduction.component,
            dmc.Divider(label="Views & Layouts"),
            section_renders.component,
            dmc.Divider(label="Header Toolbar"),
            header_toolbar.component,
            dmc.Divider(label="Advanced Workflow"),
            extra_fields.component,
            dmc.Divider(label="API-driven Calendar"),
            api_example.component,
        ],
        size="lg",
        py="xl",
    )


app.layout = dmc.MantineProvider(
    dmc.Stack(
        [
            dcc.Location(id="url"),
            dmc.Group(
                [
                    dmc.Anchor("Home", href="/", size="lg"),
                    dmc.Anchor("Full Calendar Docs", href="/pip/full_calendar_component", size="lg"),
                ],
                justify="center",
                gap="xl",
                py="md",
            ),
            html.Div(id="page-content"),
        ]
    ),
    theme={"colorScheme": "dark"},
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):
    if pathname == "/pip/full_calendar_component":
        return render_full_calendar_docs()
    return render_home()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8059)
