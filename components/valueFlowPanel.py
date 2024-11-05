import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import dash_ag_grid as dag


#################################################################

dfTrade = pd.read_csv("./data/country_trade_register_postProc.csv")

#################################################################
# components to build the army trading panel - top yearly army trades
yearsOption = sorted([int(year) for year in dfTrade["Year"].unique()])
yearsOption = list(map(str, yearsOption))

yearLabel = dbc.Label(["Year Selection"])
flowYearSlider = dcc.Dropdown(
    yearsOption,
    "2020",
    id="flowYearSlider-id",
)
df2 = dfTrade[dfTrade["Year"] == 2020].reset_index().drop(columns="index")
df2s = (
    df2.groupby(by=["Supplier"])["Value"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .loc[0:5]
)
df2r = (
    df2.groupby(by=["Recipient"])["Value"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .loc[0:10]
)
top10Suppliers = df2s.Supplier.values.tolist()
top10Recipients = df2r.Recipient.values.tolist()
nodes_name = list(set(df2.Supplier.unique().tolist() + df2.Recipient.unique().tolist()))
# nodes_id=[nodes_name.index(node) for node in nodes_name ]
df2["Sid"] = ""
df2["Rid"] = ""
for i in range(df2.shape[0]):
    # print(df2.Supplier.loc[i])
    df2.Sid.loc[i] = nodes_name.index(df2.Supplier.loc[i])
    df2.Rid.loc[i] = nodes_name.index(df2.Recipient.loc[i])
# nodes_name

df2 = df2[(df2.Recipient).isin(top10Recipients)].reset_index().drop(columns=["index"])
df3 = df2.groupby(by="Recipient")["Value"].sum().reset_index()


columnDefs = [{"field": val} for val in df3.columns]
grid = dag.AgGrid(
    id="id-grid",
    rowData=df3.to_dict("records"),
    columnDefs=columnDefs,
)

figFlow = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes_name,
                color="blue",
                align="left",
            ),
            link=dict(
                source=df2.Rid.values,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                target=df2.Sid.values,
                value=df2.Value.values,
                arrowlen=15,
            ),
        )
    ]
)
figFlow.update_layout(title_text="The Money Flow", font_size=10)
figFlow.update_layout(
    # autosize=False,
    # width=1000,
    height=800,
)
countryFlow = dcc.Graph(figure=figFlow, id="countryFlow-id")
tab1 = dbc.Tab(
    [
        dbc.Container(
            [
                dbc.Row([dbc.Col([countryFlow])], justify="center"),
            ],
            className="p-2",
        )
    ],
    label="Chart",
    className="",
)
tab2 = dbc.Tab(
    [
        dbc.Container(
            [
                dbc.Row(dbc.Col([grid]), className="", justify="center"),
                dbc.Row(dbc.Col([])),
            ],
            className="m-5",
        )
    ],
    label="Table",
    className="p-4",
)
tabs = dbc.Card(dbc.Tabs([tab1, tab2]))


flowPlotPanel = dbc.Container(
    [
        dbc.Row(dbc.Col([yearLabel, flowYearSlider], className="m-5")),
        dbc.Row(dbc.Col([tabs])),
    ],
    className="bg-secondary shadow border rounded-3   mt-2 mb-2",
)


@callback(
    Output("countryFlow-id", "figure"),
    Output("id-grid", "rowData"),
    Input("flowYearSlider-id", "value"),
    prevent_initial_call=True,
)
def yearSel(sel):

    df2 = dfTrade[dfTrade["Year"] == int(sel)].reset_index().drop(columns="index")

    df2s = (
        df2.groupby(by=["Supplier"])["Value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .loc[0:5]
    )

    df2r = (
        df2.groupby(by=["Recipient"])["Value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .loc[0:10]
    )

    top10Suppliers = df2s.Supplier.values.tolist()
    top10Recipients = df2r.Recipient.values.tolist()
    nodes_name = list(
        set(df2.Supplier.unique().tolist() + df2.Recipient.unique().tolist())
    )
    # nodes_id=[nodes_name.index(node) for node in nodes_name ]
    df2["Sid"] = ""
    df2["Rid"] = ""
    for i in range(df2.shape[0]):
        # print(df2.Supplier.loc[i])
        df2.Sid.loc[i] = nodes_name.index(df2.Supplier.loc[i])
        df2.Rid.loc[i] = nodes_name.index(df2.Recipient.loc[i])
    # nodes_name

    df2 = (
        df2[(df2.Recipient).isin(top10Recipients)].reset_index().drop(columns=["index"])
    )

    df3 = df2.groupby(by="Recipient")["Value"].sum().reset_index()

    rowData = df3.to_dict("records")

    figFlow = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes_name,
                    color="blue",
                    align="left",
                ),
                link=dict(
                    source=df2.Rid.values,
                    target=df2.Sid.values,
                    value=df2.Value.values,
                    arrowlen=15,
                ),
            )
        ]
    )
    figFlow.update_layout(title_text="The Money Flow", font_size=10)
    figFlow.update_layout(
        # autosize=False,
        # width=1000,
        height=800,
    )
    return figFlow, rowData
