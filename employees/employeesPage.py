import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq
import plotly.graph_objects as go
titleColor='black'
fontCol='rgb(247, 87, 87)'
bgCol='rgba(247, 87, 87,0.1)'
Colors=['rgba(247, 87, 87,0.4)','rgba(247, 87, 87,0.7)','rgba(247, 87, 87,0.8)','rgba(247, 87, 87,1)','#d81f1f',]
fontColDark='#d81f1f'
depts=['Data Science','UI/UX','Software Engineering','Backend Development','Frontend Development','R&D']
tenure=['Below 1','1-2','1-4','1-5','Above 5']
contracts=['Permanent','Contract']

data = pd.read_csv(
    r'./data/compItemCust.csv')
def getData():
    data['CustomerNo'] = data['CustomerNo'].astype(int)
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    return data

def errorMessage():
    return [dbc.Col(
        [
            html.I(className="far fa-window-close fa-3x",style={'color':'red'}),
            html.H5('This Chart cannot be generated due to inaccurate data'),
        ],
        style={ 
        'margin': 'auto',
        'width': '100%',
        'background-color': 'white',
        'padding': '10px',
        'height':'550px',
        'text-align':'center'
        }),
        ]

from . import general
from . import KPI
from . import advanced
from . import prediction

from app import app

# 'background-color': '#F8F8F8'


def employeesPageLayout():

    return html.Div(
        style={'padding': '15px', 'width': '100%',
               'background-color': '#f5f5f5'},
        children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="General", tab_id="General"),
                    dbc.Tab(label="Advanced", tab_id="Advanced"),
                    dbc.Tab(label="KPI", tab_id="KPI"),
                    dbc.Tab(label="Prediction", tab_id="Pred"),
                    # dbc.Tab(label="Predictions", tab_id="Prediction"),
                ],
                id="emp-tabs",
                active_tab="General",
            ),
            html.Div(id="emp-tab-content", className="mt-0"),
            #

        ]  # MAIN HTML END,
        , className='container-fluid'
    )

# Main TABS CALLBACK


@app.callback(
    Output("emp-tab-content", "children"),
    [Input("emp-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == "General":
            return general.getEmpGeneralLayout()
        elif active_tab == "Advanced":
            return advanced.getEmpAdvancedLayout()
        elif active_tab == "KPI":
            return KPI.getKPILayout()
        elif active_tab == "Pred":
            return prediction.getCustPredictionLayout()    

    return "No tab selected"
