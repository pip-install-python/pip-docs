from dash import *
import dash_mantine_components as dmc
from pathlib import Path


file_path = Path(__file__).parent / "dash_leaflet-1.0.18.tar.gz"

component = html.Div(
    [
        dmc.Center(dmc.Button("Download File", id="download-button")),
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