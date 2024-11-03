from dash import Dash, dcc, html, Input, Output, State, callback

import dash_bootstrap_components as dbc

# components to build the dashboard headers
title = html.H4(
    [
        "Global Arms Trade and Investments",
    ],
    className="bg-primary text-white shadow border rounded-3  p-3 mt-3 mb-2",
)


headerPanel = dbc.Container([title])
