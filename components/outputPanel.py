from dash import Dash, dcc, html, Input, Output, State, callback

import dash_bootstrap_components as dbc


outputPanel = dbc.Container(
    [
        dbc.Row(
            [dbc.Col([dcc.Markdown([""], className="p-3", id="id-outputPanel")])],
        ),
    ],
    className="bg-secondary shadow border rounded-3   mt-2 mb-2",
)
