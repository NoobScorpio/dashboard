import pandas as pd

titleColor='black'
fontCol='rgb(32,178,170)'
bgCol='rgba(32,178,170,0.1)'
Colors=[
    'rgba(32,178,170,0.1)',
    'rgba(32,178,170,0.2)',
    'rgba(32,178,170,0.3)',
    'rgba(32,178,170,0.4)',
    'rgba(32,178,170,0.5)',
    'rgba(32,178,170,0.6)',
    'rgba(32,178,170,0.7)',
    'rgba(32,178,170,0.8)',
    'rgba(32,178,170,0.9)',
    'rgba(32,178,170,1)',
    '#008080',
    'rgba(32,178,170,0.1)',
    'rgba(32,178,170,0.2)',
    'rgba(32,178,170,0.3)',
    'rgba(32,178,170,0.4)',
    'rgba(32,178,170,0.5)',
    'rgba(32,178,170,0.6)',
    'rgba(32,178,170,0.7)',
    'rgba(32,178,170,0.8)',
    'rgba(32,178,170,0.9)',
    'rgba(32,178,170,1)',
    '#008080',]
fontColDark='#008080'

data = pd.read_csv(
    r'./data/genData.csv')
def getData():
    data['CustomerNo'] = data['CustomerNo'].astype(int)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    return data
from . import general
from . import KPI
from . import advanced
from . import prediction
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objects as go
from app import app

# 'background-color': '#F8F8F8'


def customersPageLayout():
    print(' INSIDE CUSTOMERS PAGE LAYOUT')
    return html.Div(
        style={'padding': '15px', 'width': '100%',
               'background-color': '#F8FBF6'},
        children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="General", tab_id="General"),
                    dbc.Tab(label="Advanced", tab_id="Advanced"),
                    dbc.Tab(label="KPI", tab_id="KPI"),
                    dbc.Tab(label="Prediction", tab_id="Pred"),
                    # dbc.Tab(label="Predictions", tab_id="Prediction"),
                ],
                id="cust-tabs",
                active_tab="General",
            ),
            html.Div(id="cust-tab-content", className="p-0"),
            #

        ]  # MAIN HTML END,
        , className='container-fluid'
    )

# Main TABS CALLBACK


@app.callback(
    Output("cust-tab-content", "children"),
    [Input("cust-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "General":
            print(' INSIDE CUSTOMERS GENERAL TAB')
            return general.getCustGeneralLayout()
        elif active_tab == "Advanced":
            return advanced.getAdvancedLayout()
        elif active_tab == "KPI":
            return KPI.getKPILayout()
        elif active_tab == "Pred":
            return prediction.getCustPredictionLayout()    

    return "No tab selected"
