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
from . import suppliersPage as cP

data = cP.getData()
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors

def getSectionLayout(title="Customer Churn",thisMonth="1.42%",diff="+0.46",total="16.86%",fig=go.Figure()):
    return dbc.Col([
        dbc.Row([html.Div(f'{title}', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color':titleColor,
        })], className='d-flex justify-content-center mt-1',),
        dbc.Row(
            [

                dbc.Col([
                    dbc.Row(html.Div('Last Month', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                 'color':titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{thisMonth}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                 'color':fontCol,
                            }),
                            html.Div(f"({diff})", style={
                                'font-size': '28px',
                                'font-weight': 'normal',
                                'margin-top': '25px',
                                 'color':fontCol,
                            }),
                        ],className='d-flex justify-content-center'),
                    dbc.Row('vs. Previous Month',className='d-flex justify-content-center',style={ 'color':titleColor,}),
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
                dbc.Col([
                    
                    dbc.Row(html.Div('Total', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                 'color':titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{total}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                 'color':fontCol,
                            }),
                            
                        ],className='d-flex justify-content-center'),
                    dbc.Row('Last 12 Months',className='d-flex justify-content-center',style={ 'color':titleColor,}),
                
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),


            ], className='d-flex justify-content-center mt-1',),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig), style={
                    'margin-bottom': '10px',
                    }),


            ], className='d-flex justify-content-center mt-1',),


    ], style={
        'margin-top': '10px',
        'color': 'white',
        'margin': '10px',
        'background-color': 'white',
        'border-radius': '5px',
        'font-size': '20px', },className='mt-2')


def getSupQuanFig():
    fig=go.Figure(data=[
        go.Bar(
            y=[100,500,200,50,400],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            y=[100,500,200,50,400],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],
            marker_color=fontCol,
            name='Quantity Ordered'
        ),
        go.Line(
            y=[90,490,100,60,370],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color='green',
            name='Received'
        ),
        go.Line(
            y=[10,50,20,5,40],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color='red',
            name='defects'
        ),
        go.Line(
            y=[25,100,60,15,80],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color='blue',
            name='Returned'
        ),

    ],
    layout=go.Layout(
            xaxis=dict(
                title='<b>Weeks</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Quantity</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>Purchased Quantity from supplier</b>',
        title_font_size=20,

        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig

def getSupAvgDeliveryTimeFig():
    fig=go.Figure(data=[
        go.Bar(
            y=[1,2,1.5,0.5,1],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],     
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            y=[1,2,1.5,0.5,1],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color=fontCol,
            name='Time(Days)'
        )
    ],
    layout=go.Layout(
            xaxis=dict(
                title='<b>Months</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Delivery Time</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>Average Delivery Time</b>',
        title_font_size=20,

        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig

def getSupDefectRateFig():
    fig=go.Figure(data=[
        go.Bar(
            y=[10,50,15,0,50],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            y=[10,50,15,0,50],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color=fontCol,
            name='Quantity'
        )
    ],
    layout=go.Layout(
            xaxis=dict(
                title='<b>Weeks</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Quantity</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>Defected Items from supplier</b>',
        title_font_size=20,

        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig

def getSupOnTimeFig():
    fig=go.Figure(data=[
        go.Bar(
            y=[1,1,1.5,2,0.5],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],
            marker_color=bgCol, 
            name='Time(Days)'
        ),
        go.Line(
           y=[1,1,1.5,2,0.5],
            x=['Week 1','Week 2','Week 3','Week 4','Week 5'],            
            marker_color=fontCol,
            name='Time(Days)'
        )
    ],
    layout=go.Layout(
            xaxis=dict(
                title='<b>Weeks</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Time(Days)</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>On Time Delivery Rate</b>',
        title_font_size=20,

        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return fig


def getKPILayout():
    return [
        dbc.Row(
            [
                html.Div(getSectionLayout(title="Supplier Quantity Timeline",fig=getSupQuanFig()),className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-6"),
                html.Div(getSectionLayout(title='Avergae Delivery Time',fig=getSupAvgDeliveryTimeFig()),className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-6"),
            ]
        ),
        dbc.Row(
            [
                html.Div(getSectionLayout(title="Defect Rate",fig=getSupDefectRateFig()),className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-6"),
                html.Div(getSectionLayout(title='On-Time Delivery Rate',fig=getSupOnTimeFig()),className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-6"),
            ]
        ),
    ]