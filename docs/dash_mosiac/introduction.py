import dash_mantine_components as dmc
from dash_iconify import DashIconify

demo_py = """
import dash_mantine_components as dmc

 dmc.Checkbox(
    classNames={"root": "dmc-api-demo-root"},
    label="Checkbox button",
    w=180
)"""


code = [
    {
        "fileName": "demo.py",
        "code": demo_py,
        "language": "python",
        "icon": DashIconify(icon="skill-icons:python-dark", width=20),
    },
]

component = dmc.CodeHighlightTabs(
    code=code,
    withExpandButton=True,
    expandCodeLabel="Show full code",
    collapseCodeLabel="Show less",
    defaultExpanded=False,
    maxCollapsedHeight=200  # Height in collapsed state (in pixels)
)