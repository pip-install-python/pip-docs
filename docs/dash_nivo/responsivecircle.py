from dash import *
from dash_nivo import ResponsiveCircle
import json


data = {
  "name": "nivo",
  "color": "hsl(316, 70%, 50%)",
  "children": [
    {
      "name": "viz",
      "color": "hsl(133, 70%, 50%)",
      "children": [
        {
          "name": "stack",
          "color": "hsl(259, 70%, 50%)",
          "children": [
            {
              "name": "cchart",
              "color": "hsl(347, 70%, 50%)",
              "loc": 137984
            },
            {
              "name": "xAxis",
              "color": "hsl(24, 70%, 50%)",
              "loc": 152592
            },
            {
              "name": "yAxis",
              "color": "hsl(320, 70%, 50%)",
              "loc": 103921
            },
            {
              "name": "layers",
              "color": "hsl(165, 70%, 50%)",
              "loc": 23268
            }
          ]
        },
        {
          "name": "ppie",
          "color": "hsl(280, 70%, 50%)",
          "children": [
            {
              "name": "chart",
              "color": "hsl(115, 70%, 50%)",
              "children": [
                {
                  "name": "pie",
                  "color": "hsl(285, 70%, 50%)",
                  "children": [
                    {
                      "name": "outline",
                      "color": "hsl(344, 70%, 50%)",
                      "loc": 84293
                    },
                    {
                      "name": "slices",
                      "color": "hsl(307, 70%, 50%)",
                      "loc": 86633
                    },
                    {
                      "name": "bbox",
                      "color": "hsl(181, 70%, 50%)",
                      "loc": 92679
                    }
                  ]
                },
                {
                  "name": "donut",
                  "color": "hsl(31, 70%, 50%)",
                  "loc": 196760
                },
                {
                  "name": "gauge",
                  "color": "hsl(260, 70%, 50%)",
                  "loc": 62203
                }
              ]
            },
            {
              "name": "legends",
              "color": "hsl(352, 70%, 50%)",
              "loc": 21602
            }
          ]
        }
      ]
    },
    {
      "name": "colors",
      "color": "hsl(151, 70%, 50%)",
      "children": [
        {
          "name": "rgb",
          "color": "hsl(307, 70%, 50%)",
          "loc": 140165
        },
        {
          "name": "hsl",
          "color": "hsl(124, 70%, 50%)",
          "loc": 87801
        }
      ]
    },
    {
      "name": "utils",
      "color": "hsl(59, 70%, 50%)",
      "children": [
        {
          "name": "randomize",
          "color": "hsl(325, 70%, 50%)",
          "loc": 49221
        },
        {
          "name": "resetClock",
          "color": "hsl(127, 70%, 50%)",
          "loc": 51258
        },
        {
          "name": "noop",
          "color": "hsl(286, 70%, 50%)",
          "loc": 67154
        },
        {
          "name": "tick",
          "color": "hsl(45, 70%, 50%)",
          "loc": 190804
        },
        {
          "name": "forceGC",
          "color": "hsl(313, 70%, 50%)",
          "loc": 69121
        },
        {
          "name": "stackTrace",
          "color": "hsl(123, 70%, 50%)",
          "loc": 144408
        },
        {
          "name": "dbg",
          "color": "hsl(328, 70%, 50%)",
          "loc": 121414
        }
      ]
    },
    {
      "name": "generators",
      "color": "hsl(50, 70%, 50%)",
      "children": [
        {
          "name": "address",
          "color": "hsl(57, 70%, 50%)",
          "loc": 36337
        },
        {
          "name": "city",
          "color": "hsl(205, 70%, 50%)",
          "loc": 33309
        },
        {
          "name": "animal",
          "color": "hsl(84, 70%, 50%)",
          "loc": 116425
        },
        {
          "name": "movie",
          "color": "hsl(297, 70%, 50%)",
          "loc": 136098
        },
        {
          "name": "user",
          "color": "hsl(218, 70%, 50%)",
          "loc": 68164
        }
      ]
    },
    {
      "name": "set",
      "color": "hsl(168, 70%, 50%)",
      "children": [
        {
          "name": "clone",
          "color": "hsl(227, 70%, 50%)",
          "loc": 48576
        },
        {
          "name": "intersect",
          "color": "hsl(167, 70%, 50%)",
          "loc": 77107
        },
        {
          "name": "merge",
          "color": "hsl(320, 70%, 50%)",
          "loc": 182462
        },
        {
          "name": "reverse",
          "color": "hsl(264, 70%, 50%)",
          "loc": 47817
        },
        {
          "name": "toArray",
          "color": "hsl(240, 70%, 50%)",
          "loc": 26223
        },
        {
          "name": "toObject",
          "color": "hsl(37, 70%, 50%)",
          "loc": 146991
        },
        {
          "name": "fromCSV",
          "color": "hsl(185, 70%, 50%)",
          "loc": 146569
        },
        {
          "name": "slice",
          "color": "hsl(128, 70%, 50%)",
          "loc": 4120
        },
        {
          "name": "append",
          "color": "hsl(139, 70%, 50%)",
          "loc": 34050
        },
        {
          "name": "prepend",
          "color": "hsl(83, 70%, 50%)",
          "loc": 7894
        },
        {
          "name": "shuffle",
          "color": "hsl(252, 70%, 50%)",
          "loc": 18792
        },
        {
          "name": "pick",
          "color": "hsl(324, 70%, 50%)",
          "loc": 10420
        },
        {
          "name": "plouc",
          "color": "hsl(244, 70%, 50%)",
          "loc": 82525
        }
      ]
    },
    {
      "name": "text",
      "color": "hsl(199, 70%, 50%)",
      "children": [
        {
          "name": "trim",
          "color": "hsl(32, 70%, 50%)",
          "loc": 6602
        },
        {
          "name": "slugify",
          "color": "hsl(316, 70%, 50%)",
          "loc": 58840
        },
        {
          "name": "snakeCase",
          "color": "hsl(314, 70%, 50%)",
          "loc": 17153
        },
        {
          "name": "camelCase",
          "color": "hsl(9, 70%, 50%)",
          "loc": 26398
        },
        {
          "name": "repeat",
          "color": "hsl(83, 70%, 50%)",
          "loc": 184387
        },
        {
          "name": "padLeft",
          "color": "hsl(297, 70%, 50%)",
          "loc": 132746
        },
        {
          "name": "padRight",
          "color": "hsl(276, 70%, 50%)",
          "loc": 112487
        },
        {
          "name": "sanitize",
          "color": "hsl(343, 70%, 50%)",
          "loc": 34971
        },
        {
          "name": "ploucify",
          "color": "hsl(288, 70%, 50%)",
          "loc": 120651
        }
      ]
    },
    {
      "name": "misc",
      "color": "hsl(303, 70%, 50%)",
      "children": [
        {
          "name": "greetings",
          "color": "hsl(240, 70%, 50%)",
          "children": [
            {
              "name": "hey",
              "color": "hsl(10, 70%, 50%)",
              "loc": 140378
            },
            {
              "name": "HOWDY",
              "color": "hsl(101, 70%, 50%)",
              "loc": 196072
            },
            {
              "name": "aloha",
              "color": "hsl(240, 70%, 50%)",
              "loc": 115654
            },
            {
              "name": "AHOY",
              "color": "hsl(91, 70%, 50%)",
              "loc": 150632
            }
          ]
        },
        {
          "name": "other",
          "color": "hsl(194, 70%, 50%)",
          "loc": 118375
        },
        {
          "name": "path",
          "color": "hsl(29, 70%, 50%)",
          "children": [
            {
              "name": "pathA",
              "color": "hsl(184, 70%, 50%)",
              "loc": 192875
            },
            {
              "name": "pathB",
              "color": "hsl(47, 70%, 50%)",
              "children": [
                {
                  "name": "pathB1",
                  "color": "hsl(181, 70%, 50%)",
                  "loc": 78668
                },
                {
                  "name": "pathB2",
                  "color": "hsl(221, 70%, 50%)",
                  "loc": 26496
                },
                {
                  "name": "pathB3",
                  "color": "hsl(245, 70%, 50%)",
                  "loc": 143221
                },
                {
                  "name": "pathB4",
                  "color": "hsl(126, 70%, 50%)",
                  "loc": 140927
                }
              ]
            },
            {
              "name": "pathC",
              "color": "hsl(345, 70%, 50%)",
              "children": [
                {
                  "name": "pathC1",
                  "color": "hsl(84, 70%, 50%)",
                  "loc": 48685
                },
                {
                  "name": "pathC2",
                  "color": "hsl(96, 70%, 50%)",
                  "loc": 36693
                },
                {
                  "name": "pathC3",
                  "color": "hsl(151, 70%, 50%)",
                  "loc": 131845
                },
                {
                  "name": "pathC4",
                  "color": "hsl(51, 70%, 50%)",
                  "loc": 51025
                },
                {
                  "name": "pathC5",
                  "color": "hsl(103, 70%, 50%)",
                  "loc": 150011
                },
                {
                  "name": "pathC6",
                  "color": "hsl(99, 70%, 50%)",
                  "loc": 87012
                },
                {
                  "name": "pathC7",
                  "color": "hsl(248, 70%, 50%)",
                  "loc": 58815
                },
                {
                  "name": "pathC8",
                  "color": "hsl(202, 70%, 50%)",
                  "loc": 197659
                },
                {
                  "name": "pathC9",
                  "color": "hsl(110, 70%, 50%)",
                  "loc": 61511
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}


component = html.Div([
    html.Div(ResponsiveCircle(
        id='circle-packing',
        data=data,
        margin={'top': 20, 'right': 20, 'bottom': 20, 'left': 20},
        colors={'scheme': 'nivo'},
        childColor={
            'from': 'color',
            'modifiers': [['brighter', 0.4]]
        },
        padding=4,
        enableLabels=True,
        labelsSkipRadius=16,
        labelTextColor={
            'from': 'color',
            'modifiers': [['darker', 2]]
        },
        borderWidth=1,
        borderColor={
            'from': 'color',
            'modifiers': [['darker', 0.5]]
        },
        defs=[{
            'id': 'lines',
            'type': 'patternLines',
            'background': 'none',
            'color': 'inherit',
            'rotation': -45,
            'lineWidth': 5,
            'spacing': 8
        }],
        fill=[{
            'match': {'depth': 1},
            'id': 'lines'
        }],
        motionConfig='slow'
    ), style={'color': 'black'}),
    html.Div(id='zoom-info'),

])


@callback(
    Output('zoom-info', 'children'),
    Input('circle-packing', 'zoomedId')
)
def display_zoom_info(zoomedId):
    if zoomedId:
        return f"Zoomed to: {zoomedId}"
    return "No zoom applied"

