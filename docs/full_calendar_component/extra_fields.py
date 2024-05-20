from typing import Literal

import dash_mantine_components as dmc
from dash import Input, Output, State, callback, html



component = dmc.SimpleGrid(
    [
        dmc.Paper(
            html.H1("Hello world, extra_fields.py!"),
            id="extra-wrapper",
            style={"gridColumn": "1 / 4"},
        ),

    ],
    cols=4,
    spacing="2rem",
)


