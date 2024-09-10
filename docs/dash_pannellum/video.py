from dash import html
import dash_pannellum

component = html.Div([
    dash_pannellum.DashPannellum(
        id='panorama',
        video={
            "sources": [
                {"src": "https://bitmovin-a.akamaihd.net/content/playhouse-vr/progressive.mp4", "type": "video/mp4"},
            ],
            "poster": "https://bitmovin-a.akamaihd.net/content/playhouse-vr/poster.jpg"
        },
        autoLoad=True,
        width='100%',
        height='400px',
    )
])
