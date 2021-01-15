from . import salesPage as cP
import numpy
import pandas as pd
import datetime
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.arima_model import ARIMAResults
from pandas import DataFrame
import warnings
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from collections import OrderedDict
from operator import itemgetter
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output
# warnings.filterwarnings('ignore')
data = pd.read_csv(r'./data/total.csv')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data = data[data['InvoiceDate'] > pd.to_datetime('2019-09-01')]
series = data.Total
model_fit = ARIMAResults.load(r'./data/models/model.pkl')



titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors

def salesDifference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return numpy.array(diff)


def inverse_salesDifference(history, yhat, interval=1):
    return yhat + history[-interval]


def getWeeksData(weeksData):
    labels = []
    values = []
    # print(len(weeksData))
    if len(weeksData) <= 15:
        weeksData['InvoiceDate'] = weeksData['InvoiceDate'].astype(str)
        new_labels = list(weeksData['InvoiceDate'])
        labels = []
        for i in new_labels:
            labels.append(i.split('T')[0])
        values = list(weeksData['Total'])
        # print(labels,values)
    else:
        weeksData = weeksEval(weeksData)
        labels = list(weeksData.keys())
        values = list(weeksData.values())
        # print(labels,values)
    return labels, values


def weeksEval(month):
    # print('EVALUATING MONTH')
    weeks = [g for n, g in month.groupby(
        pd.Grouper(key='InvoiceDate', freq='W'))]
    weeks_list = []
    for week in weeks:
        weeks_list.append(pd.DataFrame(
            week.groupby('InvoiceDate').Total.sum()))
    weeks_sum_dict = {}
    i = 1
    for week in weeks_list:
        weeks_sum_dict[f"Week {i}"] = week['Total'].sum()
        i += 1
    # weeks_sum_dict=OrderedDict(sorted(weeks_sum_dict.items(), key=itemgetter(1)))
    # iterator = iter(weeks_sum_dict.items())
    # print('RETURNING EVAL MONTH')
    # return list(iterator)
    return weeks_sum_dict


def getPredictionGraph(old, new):
    old['Max'] = max(old['Total'])
    fig = go.Figure(
        data=[
            go.Line(
                marker_color="grey",
                name='Max',
                x=old.index,
                y=old['Max'],
                line=dict(color='grey', width=1,
                          dash='dash'),
            ),
            go.Line(
                marker_color='#6AC738',
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=old.index,
                y=old['Total'],
                fill='tozeroy',
                fillcolor='rgba(204, 235, 194,0.2)',
                # line={
                #     'shape': 'spline',
                #     'smoothing': 1.3
                # },
            ),
            go.Line(
                marker_color='#229bf2',
                # "rgba(137, 184, 80, 1)",
                name='Forecast',
                x=new.index,
                y=new['Total'],
                fill='tozeroy',
                fillcolor='rgba(204, 235, 194,0.2)',
                # line={
                #     'shape': 'spline',
                #     'smoothing': 1.3
                # },
            ),
        ], )
    fig.update_layout(
        # autosize=False,
        # width=2000,
        # height=480,
        title_text=f'<b></b>',
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Sales</b>",
        plot_bgcolor='rgba(0, 0, 0, 0)',)

    return dcc.Graph(figure=fig)


def getPredictionWeeks(labels, values):
    colors=[ 
        '#052B04',
        '#013423',
        '#054722',
        '#327140',
        '#204B09',
        '#084D06',
        '#41841E',
        '#11820D',
        '#008F21',
        '#48B110',
        '#79B118',
        '#13BB3A',
        '#3DC738',
        '#38C759',
        '#6EBC42',
        '#9DE576']
    colors.reverse()
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                insidetextorientation='radial',
                marker_colors=colors
            ),
        ], )
    fig.update_layout(
        showlegend=False,
        # autosize=False,
        # width=500,
        height=500,
        title_text=f'<b>Forecast Breakdown</b>',
        title_font_size=24
        # xaxis_title="",
        # yaxis_title="",
        # plot_bgcolor='rgba(0, 0, 0, 0)',
    )
    fig.update_traces(textposition='inside', textfont_size=18)
    return dcc.Graph(figure=fig)


def getDropDownItems():
    i = 0
    j = 7
    menuItems = []
    while i < 8:
        if i == 0:
            menuItems.append({'label': f"{i+1} Week", 'value': j})
        else:
            menuItems.append({'label': f"{i+1} Weeks", 'value': j})
        # menuItems.append(dbc.DropdownMenuItem(divider=True),)
        # print(monthNames[i])
        i += 1
        j += 7
    # print(f"THIS IS MONTH ARRAY LENGTH {len(menuItems)}")
    return menuItems


def getPredictionsGraphs(days):
    # multi-step out-of-sample forecast
    X = series.values
    days_in_year = 12
    salesDifferenced = salesDifference(X, days_in_year)
    start_index = len(salesDifferenced)
    print(f"LEN OF X : {len(X)}")
    end_index = start_index + int(days)
    forecast = model_fit.predict(start=start_index, end=end_index)
    print(f"forecast LENGTH : {len(forecast)} ")
    print(f"START INDEX : {start_index} and END INDEX : {end_index}")
    # invert the salesDifferenced forecast to something usable
    history = [x for x in X]
    print(f"HISTORY LENGTH : {len(history)} ")
    day = 1
    li = []
    for yhat in forecast:
        inverted = inverse_salesDifference(history, yhat, days_in_year)
        li.append(inverted)
        history.append(inverted)
        day += 1
    df = data
    print(f"Li LENGTH : {len(li)} ")
    old_history = df
    old_history.set_index(old_history['InvoiceDate'], inplace=True)

    history_index = df.index

    dti = pd.date_range('2020-07-15', periods=int(days+1))
    history_index = history_index.append(dti)
    data_history = pd.DataFrame(history)
    data_history.set_index(history_index, inplace=True)
    data_history

    data_forecast = pd.DataFrame(li, columns=['Total'])

    dti = pd.date_range('2020-07-9', periods=int(days+1))
    data_forecast.set_index(dti, inplace=True)
    data_forecast.index = pd.to_datetime(data_forecast.index)
    old_history.index = pd.to_datetime(old_history.index)
    
    weeksData = data_forecast
    weeksData['InvoiceDate'] = pd.to_datetime(weeksData.index)
    labels, values = getWeeksData(weeksData)

    return (
        getPredictionGraph(old_history, data_forecast),
        getPredictionWeeks(labels, values),
    )


def get15DaysPredictionBars(data_forecast):
    fig = go.Figure(
        data=[
            go.Bar(
                marker_color=  # 'red',
                '#6AC738',
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=data_forecast.index,
                y=data_forecast['Total'],
            ),
        ], )
    fig.update_layout(
        # autosize=False,
        # width=2000,
        height=500,
        title_text=f'<b>15 Days Forecast</b>',
        title_font_size=24,
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Sales</b>",
        plot_bgcolor='rgba(0, 0, 0, 0)',)

    return dcc.Graph(figure=fig)


def get15DaysPrediction():
    # multi-step out-of-sample forecast
    X = series.values
    days_in_year = 12
    salesDifferenced = salesDifference(X, days_in_year)
    start_index = len(salesDifferenced)
    end_index = start_index + 14
    forecast = model_fit.predict(start=start_index, end=end_index)
    # invert the salesDifferenced forecast to something usable
    history = [x for x in X]
    day = 1
    li = []
    for yhat in forecast:
        inverted = inverse_salesDifference(history, yhat, days_in_year)
        li.append(inverted)
        history.append(inverted)
        day += 1
    df = data
    old_history = df
    old_history.set_index(old_history['InvoiceDate'], inplace=True)
    # old_history.drop(columns=['InvoiceDate'],inplace=True)
    old_history
    history_index = df.index
    history_index
    dti = pd.date_range('2020-07-15', periods=15)
    history_index = history_index.append(dti)
    data_history = pd.DataFrame(history)
    data_history.set_index(history_index, inplace=True)
    data_history

    data_forecast = pd.DataFrame(li, columns=['Total'])

    dti = pd.date_range('2020-07-14', periods=15)
    data_forecast.set_index(dti, inplace=True)
    data_forecast.index = pd.to_datetime(data_forecast.index)
    old_history.index = pd.to_datetime(old_history.index)

    return get15DaysPredictionBars(data_forecast)


# MAIN


def getPredictions():
    #
    return [
        dbc.Row([
            dbc.Col([
                html.Div([

                    dbc.Row(
                       [ 
                           
                           dbc.Col(html.Div("Sales Forecast", style={
                                            'margin-right': '30px',
                                            'font-size': '24px',
                                            'font-weight': 'bold',
                                            'color': titleColor,
                                            'margin-top': '-30px',
                                        }), width=6, className="d-flex justify-content-start p-5"),
                           dbc.Col(
                            [

                                dbc.Row(
                                    [
                                        html.Div('Select Week', style={
                                            'margin-right': '30px',
                                            'font-size': '24px',
                                            'font-weight': 'bold',
                                            'color': titleColor,
                                            'margin-top': '-30px',
                                        }),
                                        dcc.Dropdown(
                                            id='predictionDropDown',
                                            options=getDropDownItems(),
                                            value=7,
                                            searchable=False,
                                            style={'width': '150px',
                                                   'margin-top': '-14px', }
                                        )
                                    ]
                                ),

                            ], width=6, className="d-flex justify-content-end p-5"),
                            
                            
                            ]
                            
                            ),

                    dbc.Row(dbc.Col(html.Div(id='predcitionTimeLine',
                                             style={'margin-top': '-45px', }), width=12)),

                ], style={
                    'margin': '10px',
                    # 'padding':'10px',
                    'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                    'background-color': 'white',
                    # 'height':'500',
                    # 'width':'100%'
                })
            ], width=12),
        ]),
        dbc.Row([
            html.Div([
                    html.Div(id='predcitionBars', style={
                        'margin-left': '10px',
                        # 'padding':'10px',
                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        'background-color': 'white',
                        # 'height':'500',
                        # 'width': '100%'
                    })
                    ], className='mt-3 col-sm-12 col-md-12 col-lg-5 col-xl-5'),
            html.Div([
                    html.Div(get15DaysPrediction(), style={
                        'margin-right': '10px',
                        # 'padding':'10px',
                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        'background-color': 'white',
                        # 'height':'500',
                        # 'width':'100%'
                    })
                    ], className='mt-3 col-sm-12 col-md-12 col-lg-7 col-xl-7'),
        ])
    ]


@app.callback(
    Output("predcitionTimeLine", "children"),
    Output("predcitionBars", "children"),

    [Input("predictionDropDown", "value")],
)
def predcitionTimeLineFunction(value):
    if value == None:
        value = 7
    return getPredictionsGraphs(value)
