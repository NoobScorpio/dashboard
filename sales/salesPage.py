import sys
sys.path.append("..") 
sys.path.append(".") 
titleColor='black'
fontCol='#89B850'
bgCol='rgba(28, 166, 230,0.1)'
Colors=['#1a5a78','#247ba3','#2e98c9','#1ca6e6','#0fb3ff',]
fontColDark='#0e719e'
from sales import localize
# from localize import headerEnDict,localize.headerArDict

headerEnDictGen=localize.headerEnDict
headerArDictGen=localize.headerArDict
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from sales import general as sales
from sales import customersFunctions as cust
from sales import itemsFunctions as itemsF
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objects as go
from sales import advanced as aSec
from sales import KPI as KPI
from sales import predictionFunctions as predF
from app import app






# 'background-color': '#F8F8F8'
def salesPageLayout():
    return html.Div(
        style={'padding': '15px', 'width': '100%',
               'background-color': '#F8F8F8'},
        children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="General", tab_id="General"),
                    dbc.Tab(label="Advanced", tab_id="Advanced"),
                    dbc.Tab(label="KPI", tab_id="KPI"),
                    dbc.Tab(label="Predictions", tab_id="Prediction"),
                ],
                id="sales-tabs",
                active_tab="General",
            ),
            html.Div(id="sales-tab-content", className="p-0"),
            #

        ]  # MAIN HTML END,
        , className='container-fluid'
    )

# Main TABS CALLBACK


@app.callback(
    Output("sales-tab-content", "children"),
    [Input("sales-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "General":
            return sales.salesGeneralTab()
        elif active_tab == "Advanced":
            return aSec.salesAdvancedTab()
        elif active_tab == "KPI":
            return KPI.getKPI()
        elif active_tab == "Prediction":
            return predF.getPredictions()
    return "No tab selected"
