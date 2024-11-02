from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
import dash_bootstrap_components as dbc

#######################################################
import warnings

warnings.filterwarnings(action="ignore")

#######################################################
from components.headerPanel import headerPanel
from components.inputPanel import inputPanel
from components.outputPanel import outputPanel
from components.milexPanel import countryPlotPanel
from components.valueFlowPanel import flowPlotPanel

#######################################################
from tools.tool import (
    search,
    retriever_tool,
    wikipedia_tool,
    milex_tool,
    start_tool,
    trading_tool,
    dataStore,
)

#######################################################
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage

#######################################################
from utils.support import getEnvVar

######################
OPENAI_API_KEY = getEnvVar()
##################

tools = [search, retriever_tool, wikipedia_tool, milex_tool, start_tool, trading_tool]
model = ChatOpenAI(model="gpt-4o", temperature=0)
system_prompt = """You are a helpful assistant named Doc. Your preference is to use available {tools} instead of try to answer by yourself
Assistant also doesn't know information about content on webpages and should always check if asked.

Add short notice max 150 words according with the action you take. 
Plese re-elaborate in friendly tone any piece of text you got from your actions.


Overall, you are a powerful assistant that can help to learn more about Nations military expenditures, today and historical facts about countries and the arms transfers and army deals between countries. You can help to provide valuable insights and information.
 Whether the user needs help with a specific question or just want to have a conversation about a particular topic, you is here to assist.
"""
graph = create_react_agent(
    model, tools, state_modifier=system_prompt, checkpointer=MemorySaver()
)
config = {"configurable": {"thread_id": "thread-2"}}

################################################################


# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
#

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.MORPH, dbc.icons.FONT_AWESOME],  # , dbc_css],
)


mainDataPanel = dbc.Container([], id="id-mainDataPanel")
emptyPanel = dbc.Container([], className="m-5")
app.layout = dbc.Container(
    [
        dataStore,
        headerPanel,
        dbc.Row(
            [
                dbc.Col(
                    [
                        inputPanel,
                    ],
                    width=10,
                ),
                # dbc.Col([tabs, colors], width=8),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        outputPanel,
                    ],
                    width=10,
                ),
                # dbc.Col([tabs, colors], width=8),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        mainDataPanel,
                    ],
                    width=10,
                ),
                # dbc.Col([tabs, colors], width=8),
            ],
            justify="center",
        ),
    ],
    fluid=False,
    className=" dbc dbc-ag-grid",
)


@callback(
    Output("id-outputPanel", "children"),
    Output("id-mainDataPanel", "children"),
    Input("id-submitButton", "n_clicks"),
    State("id-inputArea", "value"),
    # State("data-store", "data"),
    prevent_initial_call=True,
)
def test_out(n, value):
    print("here")
    # inputs = {"messages": [("user", "what about this app. What I can learn with it?")]}
    inputs = {"messages": [("user", f"{value}")]}
    print(config["configurable"]["thread_id"])

    for s in graph.stream(inputs, config, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

    outText = list(graph.get_state_history(config))[0].values["messages"][-1].content
    print(outText)

    if dataStore.data == "milex":
        valStore = countryPlotPanel
    elif dataStore.data == "trading":
        valStore = flowPlotPanel
    else:
        valStore = emptyPanel
    return outText, valStore


# @callback(
#     Output("id-outputPanel", "children"),
#     Input("id-resetButton", "n_clicks"),
#     prevent_initial_call=True,
# )
# def exportData(n):
#     outText = "export Done"

#     for t in list(graph.get_state_history(config))[0].values["messages"]:
#         print(t.content)
#     return outText


if __name__ == "__main__":
    app.run_server(
        debug=True, dev_tools_ui=False, dev_tools_props_check=False, port=8000
    )
