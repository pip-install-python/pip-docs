import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html
excluded_links = [
    "/404",
    "/getting-started",
    "/styles-api",
    "/style-props",
    "/dash-iconify",
    "/",
    "/migration",
    "/learning-resources",
]

category_data = {
    "API": {"icon": "material-symbols:trackpad-input-rounded"},
}

def create_content(data):

    body = []
    for entry in data:
        if entry["path"] not in excluded_links:
            link = dmc.Anchor(
                [DashIconify(icon=entry["icon"], height=20), entry["name"]],
                href=entry["path"],
                className="navbar-link",
            )
            body.append(link)

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(gap=0, children=[
            dmc.Anchor([DashIconify(icon="fluent:star-24-regular", height=20), "Introduction"], href="/", className="navbar-link",),
            dmc.Divider(label="Components", mt="2rem", mb="1rem", labelPosition="left", pl="1rem"),
            *body[::-1],
            dmc.Divider(label="Awesome Dash", mt="2rem", mb="1rem", labelPosition="left", pl="1rem"),
            dmc.Anchor([DashIconify(icon="carbon:ibm-z-os-package-manager", height=20), "PyPi Components"], href="https://community.plotly.com/t/community-components-index/60098",
                       className="navbar-link", ),
            dmc.Anchor([DashIconify(icon="streamline:global-learning", height=20), "Learning Resources"], href="/learning-resources",
                       className="navbar-link", ),
            dmc.Divider(label="Projects", mt="2rem", mb="1rem", labelPosition="left", pl="1rem"),
            dmc.Anchor(
                [DashIconify(icon='emojione:department-store', height=20), 'Store'],
                href='https://pipinstallpython.pythonanywhere.com/catalogue/',
                className="navbar-link",
            ),
            dmc.Anchor(
                [DashIconify(icon='emojione:world-map', height=20), 'GeoMapIndex'],
                href='https://dash.geomapindex.com',
                className="navbar-link",
            ),
            dmc.Divider(label="Contact", mt="2rem", mb="1rem", labelPosition="left", pl="1rem"),
            dmc.Anchor(
                [DashIconify(icon='openmoji:mobile-message', height=20), 'Message Me'],
                href='https://pipinstallpython.pythonanywhere.com/home/direct_message/',
                className="navbar-link",
            ),
        ], px="1rem", py="2rem"),
    )


def create_navbar(data):
    return dmc.AppShellNavbar(children=create_content(data))


def create_navbar_drawer(data):
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayProps={"opacity": 0.55, "blur": 3},
        zIndex=1500,
        offset=10,
        radius="md",
        withCloseButton=False,
        size="75%",
        children=create_content(data),
        trapFocus=False,
    )
