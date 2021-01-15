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
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
error=cP.errorMessage()
depts=cP.depts
tenure=cP.tenure
contracts=cP.contracts
boxStyle={
    'background-color':bgCol,
    'padding':'15px'
}
colStyle={
    'margin':'0px'
}
valueStyle={
    'text-align':'center',
    'font-weight':'bold',
    'color':fontCol
}
def getEmployeeByDept():
    try:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=depts,
                    y=[20,15,5,55,25,35],
                    marker_color=fontCol,
                    # name=name,
                )
            ],
            layout=go.Layout(
                xaxis=dict(
                    title='<b>Departments</b>',
                    titlefont=dict(
                        # family='Courier New, monospace',
                        size=18,
                        color=titleColor
                    )
                ),
                yaxis=dict(
                    title=f'<b>No. of Employees</b>',
                    titlefont=dict(
                        # family='Courier New, monospace',
                        size=18,
                        color=titleColor
                    )
                )
            )
        )
        fig.update_layout(
            title_text=f'<b>Total Employees by Departments</b>',
            title_font_color=titleColor,
            title_font_size=22,
            bargap=0.15,
            height=550,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        return dcc.Graph(figure=fig)
    except:
        return error

def getEmployeeByTenure():
    try:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=[30,15,55,25,5],
                    y=tenure,
                    marker_color=fontCol,
                    orientation='h',
                    # name=name,
                )
            ],
            layout=go.Layout(
                xaxis=dict(
                    title='<b>No. of Employees</b>',
                    titlefont=dict(
                        # family='Courier New, monospace',
                        size=18,
                        color=titleColor
                    )
                ),
                yaxis=dict(
                    title=f'<b>Tenure</b>',
                    titlefont=dict(
                        # family='Courier New, monospace',
                        size=18,
                        color=titleColor
                    )
                )
            )
        )
        fig.update_layout(
            title_text=f'<b>Total Employees by Tenure</b>',
            title_font_color=titleColor,
            title_font_size=22,
            bargap=0.15,
            height=550,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        return dcc.Graph(figure=fig)
    except:
        return error

def getEmployeeByContract():
    try:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=contracts, 
                    values=[25,135], 
                    textinfo='label+percent',
                    marker_colors=colors
                    )])
        fig.update_layout(
            title_text=f'<b>Employees by Contract Type</b>',
            title_font_color=titleColor,
            title_font_size=22,
            bargap=0.15,
            height=550,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        return dcc.Graph(figure=fig)
    except:
        return error

def getDemographic():
    try:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=['Females','Males'], 
                    values=[55,115], 
                    textinfo='label+percent',
                    marker_colors=colors
                    )])
        fig.update_layout(
            title_text=f'<b>Employees Demographics</b>',
            title_font_color=titleColor,
            title_font_size=22,
            bargap=0.15,
            height=550,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,  # gap between bars of the same location coordinate.
            paper_bgcolor='white',
            plot_bgcolor='white',
        )
        return dcc.Graph(figure=fig)
    except:
        return error

def topRow():
    return dbc.Row(
            [
               html.Div(
                    html.Div([
                        html.H4('Total Employees',style={'color':titleColor}),
                        html.H1('175',style=valueStyle)],
                        style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
                     
               html.Div(
                    html.Div([
                        html.H4('Total Salary'),
                        html.H1('$154.5k',style=valueStyle)],
                        style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
                 html.Div(
                    html.Div([
                        html.H4('Average Salary'),
                        html.H1('$1.5k',style=valueStyle)],
                         style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
                 html.Div(
                    html.Div([
                        html.H4('Maximum Salary'),
                        html.H1('$8.5k',style=valueStyle)],
                         style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
                html.Div(
                    html.Div([
                        html.H4('Total Bonus'),
                        html.H1('$55k',style=valueStyle)],
                        style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
                        html.Div(
                    html.Div([
                        html.H4('Total Overtime'),
                        html.H1('$85.7k',style=valueStyle)],
                        style=boxStyle),style=colStyle,className="mt-2 col-sm-4 col-md-4 col-lg-4 col-xl"),
            ],
           className='mt-1'
        )

def secondRow(): 
    return dbc.Row(
        [
            html.Div(getEmployeeByDept(),className="mt-1 col-sm-12 col-md-12 col-lg-12 col-xl-8"),
            html.Div(getEmployeeByTenure(),className="mt-1 col-sm-12 col-md-12 col-lg-12 col-xl-4"),
        ],
    className='mt-1'
    )

def thirdRow():
    return dbc.Row(
        [
            html.Div(getDemographic(),className="mt-1 col-sm-6 col-md-6 col-lg-4"),
            html.Div(getEmployeeByContract(),className="mt-1 col-sm-6 col-md-6 col-lg-4"),
            html.Div([
                html.Div( [

                html.Div(html.Img(src=app.get_asset_url('pie-chart-.png'),style={'height':'300px','margin-top':'90px',}),
                style={'width':'100%','display':'flex',
                'align-items':'center',
                
                'justify-content':'center'}),
                
                html.Div('This chart cannot be displayed due to inaccurate data',style={'display':'block','width':'100%','margin-top':'15px','font-weight':'bold'},className="text-center")
                
                ],style={
                'background-color':'white',
                'height':'550px',
                },className="col",

            ),
            
                
            ],className="mt-1 col-sm-6 col-md-6 col-lg-4"),

        ],
     className='mt-1'
    )   

def getEmpGeneralLayout():
    return [
        topRow(),
        secondRow(),
        thirdRow(),
    ]