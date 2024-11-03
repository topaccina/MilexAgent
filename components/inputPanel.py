from dash import Dash, dcc, html, Input, Output, State, callback

import dash_bootstrap_components as dbc

# component to build the input panel - for user query, start and close the conversation.
# End button allows to download the full chat history.
inputTitle = html.H4(
    ["Explore the landscape of arms trade and military spending with AI at your side"],
    className=" mt-2  p-3 ",
)

inputArea = html.Div(
    [
        dbc.Textarea(
            className="mb-3 mt-1 p-3 ",
            placeholder="Chat with your assistant, ask help here.",
            size="sm",
            id="id-inputArea",
        ),
        dbc.ButtonGroup(
            [
                dbc.Button(["Submit"], id="id-submitButton"),
                dbc.Button(["End"], id="id-endButton"),
            ],
            className="mb-2",
        ),
    ],
)

inputPanel = dbc.Container(
    [
        dbc.Row(
            [dbc.Col([inputTitle])],
        ),
        dbc.Row([dbc.Col([inputArea], width=10)], justify="center"),
    ],
    className="bg-secondary shadow border rounded-3   mt-2 mb-2",
)
