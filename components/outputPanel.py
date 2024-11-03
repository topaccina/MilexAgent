from dash import Dash, dcc, html, Input, Output, State, callback

import dash_bootstrap_components as dbc

# components to build AI output panel to show LLM comment on produced outputs
outputPanel = dbc.Container(
    [
        dbc.Row(
            [dbc.Col([dcc.Markdown([""], className="p-3", id="id-outputPanel")])],
        ),
    ],
    className="bg-secondary shadow border rounded-3   mt-2 mb-2",
)
