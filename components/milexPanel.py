import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc

#################################################################

dfCountry = pd.read_csv("./data/CountryExp2022GDP.csv")

#################################################################

# components to build the country MILEX expenditure panels (GDP shares, Yearly countries expenditures)
metricLabel = dbc.Label("Metric Selection")
countryCheckList = dcc.Dropdown(
    dfCountry.Country.unique(),
    dfCountry[dfCountry.Country.isin(["France", "Italy"])]["Country"].unique(),
    multi=True,
    id="id-countryCheckList",
)
countryLabel = dbc.Label("Countries Selection")
countryParDropDown = dcc.Dropdown(
    ["shareGDP", "Expenditure"],
    "shareGDP",
    id="id-countryParDropDown",
)
figCountry = px.line(
    x=dfCountry[dfCountry.Country.isin(["France", "Italy"])].Year,
    y=dfCountry[dfCountry.Country.isin(["France", "Italy"])].shareGDP,
    color=dfCountry[dfCountry.Country.isin(["France", "Italy"])].Country,
    markers=True,
)
figCountry.update_layout(
    title="Military spending as a share of GDP",
    xaxis_title="Year",
    yaxis_title="GDP Shares %",
    xaxis=dict(rangeslider=dict(visible=True), type="date"),
    xaxis_rangeslider_thickness=0.01,
)

figMap = px.choropleth(
    dfCountry,
    locations="isoAlphaCode",
    color="shareGDP",  # lifeExp is a column of gapminder
    hover_name="Country",  # column to add to hover information
    color_continuous_scale=px.colors.sequential.Blues,
    animation_frame="Year",
    # title="Military spending as a share of GDP",
)


figMap.update_layout(
    # title_text="Military spending as a share of GDP",
    geo=dict(showframe=False, showcoastlines=False),
    margin=dict(l=20, r=20, b=20, t=20, autoexpand=True),
    height=600,
)

countryPlot = dcc.Graph(figure=figCountry, id="id-countryPlot")
countryMap = dcc.Graph(figure=figMap, id="id-countryMap")

tab1 = dbc.Tab(
    [
        dbc.Container(
            [
                dbc.Row(dbc.Col([countryLabel, countryCheckList], className="p-4")),
                dbc.Row(dbc.Col([countryPlot])),
            ]
        )
    ],
    label="Chart",
    className="p-4",
)
tab2 = dbc.Tab([countryMap], label="Map", className="p-4")

tabs = dbc.Card(dbc.Tabs([tab2, tab1]))


countryPlotPanel = dbc.Container(
    [
        dbc.Row(dbc.Col([metricLabel, countryParDropDown], className="m-5")),
        dbc.Row(dbc.Col([tabs])),
    ],
    className="bg-secondary shadow border rounded-3   mt-2 mb-2",
)


@callback(
    [Output("id-countryPlot", "figure"), Output("id-countryMap", "figure")],
    [Input("id-countryCheckList", "value"), Input("id-countryParDropDown", "value")],
    prevent_initial_call=True,
)
def countrySel(sel, par):
    if not sel:
        raise PreventUpdate

    titleDict = {
        "shareGDP": "Military expenditure (pct of GDP)",
        "shareGovSpending": "Military expenditure (pct of Government Speding)",
        "Expenditure": "Military Spending -constant 2022 USD adjusted",
    }
    figCountry = px.line(
        x=dfCountry[dfCountry.Country.isin(sel)].Year,
        y=dfCountry[dfCountry.Country.isin(sel)][par],
        color=dfCountry[dfCountry.Country.isin(sel)].Country,
        markers=True,
    )
    figCountry.update_layout(
        title=titleDict[par],
        xaxis_title="Year",
        yaxis_title=par,
        xaxis=dict(rangeslider=dict(visible=True), type="date"),
        xaxis_rangeslider_thickness=0.01,
    )

    color_par = ""
    if par == "Expenditure":
        color_par = "Expenditure_log"
        dfCountry.Expenditure_log = dfCountry.Expenditure_log.astype(float)
    else:
        color_par = "shareGDP"

    figMap = px.choropleth(
        dfCountry,
        locations="isoAlphaCode",
        color=color_par,  # lifeExp is a column of gapminder
        hover_name="Country",  # column to add to hover information
        color_continuous_scale=px.colors.sequential.Blues,
        animation_frame="Year",
        # title="Military spending as a share of GDP",
    )

    figMap.update_layout(
        # title_text="Military spending as a share of GDP",
        geo=dict(showframe=False, showcoastlines=False),
        margin=dict(l=20, r=20, b=20, t=20, autoexpand=True),
        height=600,
    )
    return figCountry, figMap
