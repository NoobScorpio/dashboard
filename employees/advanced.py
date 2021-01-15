import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from collections import OrderedDict
from operator import itemgetter
import dash_daq as daq
from app import app
from dash.dependencies import Input, Output
from . import employeesPage as cP

data = cP.getData()
titleColor = cP.titleColor
fontCol = cP.fontCol
fontColDark = cP.fontColDark
bgCol = cP.bgCol
colors = cP.Colors
error = cP.errorMessage()
depts = cP.depts
tenure = cP.tenure
contracts = cP.contracts
boxStyle = {
    'background-color': bgCol,
    'padding': '15px'
}
colStyle = {
    'margin': '0px'
}
valueStyle = {
    'text-align': 'center',
    'font-weight': 'bold',
    'color': fontCol
}


def selectRow():
    return dbc.Row(
        [

            html.H2('Select Employee'),
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': 'Alex Rose', 'value': 0},
                    {'label': 'Martini Marcel', 'value': 1},
                    {'label': 'Sara Johns', 'value': 2}
                ],
                value=0,
                style={'width':'200px','margin-left':'15px','margin-top':'2px'}
            ),

        ],
        className='d-flex mt-1 justify-content-center'
    )

def topRow():
    return dbc.Row(
        [
            html.Div(className="mt-1 col-sm-12 col-md-12 col-lg-12 col-xl-8"),
            html.Div(className='mt-1 col-sm-12 col-md-12 col-lg-12 col-xl-4'),
        ],
        className='mt-1'
    )

def getEmpAdvancedLayout():
    return [
        selectRow(),
    ]
