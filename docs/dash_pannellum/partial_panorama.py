from dash import html
import dash_pannellum

component = html.Div([
    dash_pannellum.DashPannellum(
        id='partial-panorama-component',
        tour={"default": {"firstScene": "scene1"}, "scenes": {"scene1":
                    {
                        "type": "equirectangular",
                        "panorama": "https://archive.org/download/SalinaKansas1916Postcard/Salina%20Kansas%2C%201916%20Postcard%2C%20Front.jpg",
                        "haov": 149.87,
                        "vaov": 54.15,
                        "vOffset": 1.17
                    }
                }
              },
        width='100%',
        height='400px',
        autoLoad=True
    )
])
