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
import numpy
from statsmodels.tsa.arima_model import ARIMAResults
from . import itemsPage as cP
data = cP.getData()
data = data[data['InvoiceDate'] > pd.to_datetime('2019-09-01')]
data = data.rename(columns={'Total': 'oldTotal', 'TotalPrice': 'Total'})
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
selectedItem=[1077]

modelDict={}
modelDict[1077]=r'./data/models/item_one_model.pkl'
modelDict[3411]=r'./data/models/item_two_model.pkl'
modelDict[1616]=r'./data/models/item_three_model.pkl'
modelDict[1086]=r'./data/models/item_four_model.pkl'
modelDict[1852]=r'./data/models/item_five_model.pkl'

itemDataDict={}
itemDataDict[1077]   =r'./data/models/data/item_one.csv'
itemDataDict[3411]   =r'./data/models/data/item_two.csv'
itemDataDict[1616]   =r'./data/models/data/item_three.csv'
itemDataDict[1086]   =r'./data/models/data/item_four.csv'
itemDataDict[1852]   =r'./data/models/data/item_five.csv'

def getItemDropDownItems():
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

def itemDifference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        
        diff.append(value)
    return numpy.array(diff)

def inverse_itemDifference(history, yhat, interval=1):
    return yhat + history[-interval]

def getPredictionGraph(old, new):
    old['Max'] = max(old['Qnty'])
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
                marker_color=fontCol,
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=old.index,
                y=old['Qnty'],
                fill='tozeroy',
                fillcolor=bgCol,
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),
            go.Line(
                marker_color=fontColDark,
                # "rgba(137, 184, 80, 1)",
                name='Forecast',
                x=new.index,
                y=new['Qnty'],
                fill='tozeroy',
                fillcolor=bgCol,
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),
        ],layout=go.Layout(
            xaxis=dict(
                title='<b>Date</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Sales</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ) )
    fig.update_layout(
        # autosize=False,
        # width=2000,
        # height=480,
        title_text=f'<b></b>',
        title_font_color=titleColor,
        plot_bgcolor='rgba(0, 0, 0, 0)',)

    return dcc.Graph(figure=fig)

def getPredictionWeeks(labels, values):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                insidetextorientation='radial',
                 marker=dict(
                     colors=
                     [
                        '#3a535e',
                        '#486978',
                        '#50818f',
                        '#326278',
                        '#347694',
                        '#4791a6',
                        '#2785b0',
                        '#0081bd',
                        '#1d9bbf',
                        '#129fe0',
                        '#00afff',
                        '#167cdb',
                        '#2391f7',
                        '#40c8ed',
                        '#1bb4de',
                        '#86cfe3',
                        ], )
            )
        ], )
    fig.update_layout(
        showlegend=False,
        # autosize=False,
        # width=500,
        height=500,
        title_text=f'<b>Forecast Breakdown</b>',
        title_font_size=24,
        title_font_color=titleColor,
    )
    fig.update_traces(textposition='inside', textfont_size=16)
    return dcc.Graph(figure=fig)

def weekItemEval(month):
    # print('EVALUATING MONTH')
    weeks = [g for n, g in month.groupby(
        pd.Grouper(key='InvoiceDate', freq='W'))]
    weeks_list = []
    for week in weeks:
        weeks_list.append(pd.DataFrame(
            week.groupby('InvoiceDate').Qnty.sum()))
    weeks_sum_dict = {}
    i = 1
    for week in weeks_list:
        weeks_sum_dict[f"Week {i}"] = week['Qnty'].sum()
        i += 1
    # weeks_sum_dict=OrderedDict(sorted(weeks_sum_dict.items(), key=itemgetter(1)))
    # iterator = iter(weeks_sum_dict.items())
    # print('RETURNING EVAL MONTH')
    # return list(iterator)
    return weeks_sum_dict

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
        values = list(weeksData['Qnty'])
        # print(labels,values)
    else:
        weeksData = weekItemEval(weeksData)
        labels = list(weeksData.keys())
        values = list(weeksData.values())
        # print(labels,values)
    return labels, values

def getCustPredictionsGraphs(days):
    model_fit = ARIMAResults.load( modelDict[selectedItem[-1]] )
    itemData=data[data['ItemNo']==selectedItem[-1]]
    itemData.sort_values(by='InvoiceDate',inplace=True)
    itemData=pd.DataFrame(itemData.groupby('InvoiceDate').Qnty.sum())
    # itemData['InvoiceDate']=itemData.index
    itemData.reset_index(inplace=True)
    # itemData.drop(columns=['index'],inplace=True)
    # itemData=pd.read_csv(itemData)
    
    # print(itemData)
    itemData['InvoiceDate']=pd.to_datetime(itemData['InvoiceDate'])
    series = itemData[itemData['InvoiceDate'] > pd.to_datetime('2019-09-01')]
    # print(series)
    series=series['Qnty']
    X = series.values
    # print(f"X LENGTH {len(X)}")
    # print(X)
    days_in_year = 12
    itemDifferenced = itemDifference(X, days_in_year)
    start_index = len(itemDifferenced)
    end_index = start_index + int(days)
    # print(f"START INDEX : {start_index} and END INDEX : {end_index}")
    forecast = model_fit.predict(start=start_index, end=end_index)
    # print(f"forecast LENGTH {len(forecast)}")
    history = [x for x in X]
    day = 1
    li = []
    # print(f"HISTORY LENGTH {len(history)}")
    for yhat in forecast:
        inverted = inverse_itemDifference(history, yhat, days_in_year)
        li.append(inverted)
        history.append(inverted)
        day += 1
    df = itemData

    old_history = df
    old_history.set_index(old_history['InvoiceDate'], inplace=True)
    # print(f"Li LENGTH : {len(li)} ")
    history_index = df.index
    # print(history_index)
    dti = pd.date_range('2020-07-15', periods=int(days+1))
    # print(dti)
    # history_index = history_index.append(dti)
    data_history = pd.DataFrame(old_history)
    data_history.set_index(history_index, inplace=True)

    data_forecast = pd.DataFrame(li, columns=['Qnty'])
    # print(data_forecast)
    dti = pd.date_range('2020-07-14', periods=int(days+1))
    data_forecast.set_index(dti, inplace=True)
    data_forecast.index = pd.to_datetime(data_forecast.index)
    old_history.index = pd.to_datetime(old_history.index)
    
    weeksData = data_forecast
    print('WEEEEEKSSS DATA')
    print(weeksData)
    weeksData['InvoiceDate'] = pd.to_datetime(weeksData.index)
    labels, values =getWeeksData(weeksData)
    # print(data_forecast)
    data_forecast[data_forecast['Qnty'] < 0] = 0
    
    return (
        getPredictionGraph(old_history, data_forecast),
        getPredictionWeeks(labels, values),
    )

def get15DaysPredictionBars(data_forecast):
    fig = go.Figure(
        data=[
            go.Bar(
                marker_color=  # 'red',
                fontCol,
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=data_forecast.index,
                y=data_forecast['Qnty'],
            ),
        ],layout=go.Layout(
            xaxis=dict(
                title='<b>Date</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Sales</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ) )
    fig.update_layout(
        # autosize=False,
        # width=2000,
        height=500,
        title_text=f'<b>15 Days Forecast</b>',

        title_font_color=titleColor,
        title_font_size=24,
        plot_bgcolor='rgba(0, 0, 0, 0)',)
    print("RETURNING !15 DAYS GRAPH")
    return dcc.Graph(figure=fig)

def get15DaysPrediction():
    # multi-step out-of-sample forecast
    # print(f"SELECTED CUSTOMER is {selectedItem[-1]}" )
    model_fit = ARIMAResults.load( modelDict[selectedItem[-1]] )
    itemData=data[data['ItemNo']==selectedItem[-1]]
    itemData.sort_values(by='InvoiceDate',inplace=True)
    itemData=pd.DataFrame(itemData.groupby('InvoiceDate').Qnty.sum())
    # itemData['InvoiceDate']=itemData.index
    itemData.reset_index(inplace=True)
    # itemData.drop(columns=['index'],inplace=True)
    # itemData=pd.read_csv(itemData)
    
    print(itemData)
    itemData['InvoiceDate']=pd.to_datetime(itemData['InvoiceDate'])
    series = itemData[itemData['InvoiceDate'] > pd.to_datetime('2019-09-01')]
    # print(series)
    series=series['Qnty']
    X = series.values
    # print(f"X LENGTH {len(X)}")
    # print(X)
    days_in_year = 12
    itemDifferenced = itemDifference(X, days_in_year)
    start_index = len(itemDifferenced)
    end_index = start_index + 15
    # print(f"START INDEX : {start_index} and END INDEX : {end_index}")
    forecast = model_fit.predict(start=start_index, end=end_index)
    # print(f"forecast LENGTH {len(forecast)}")
    history = [x for x in X]
    day = 1
    li = []
    # print(f"HISTORY LENGTH {len(history)}")
    for yhat in forecast:
        inverted = inverse_itemDifference(history, yhat, days_in_year)
        li.append(inverted)
        history.append(inverted)
        day += 1
    df = itemData

    old_history = df
    old_history.set_index(old_history['InvoiceDate'], inplace=True)
    # print(f"Li LENGTH : {len(li)} ")
    history_index = df.index
    # print(history_index)
    dti = pd.date_range('2020-07-15', periods=16)
    # print(dti)
    # history_index = history_index.append(dti)
    data_history = pd.DataFrame(old_history)
    data_history.set_index(history_index, inplace=True)

    data_forecast = pd.DataFrame(li, columns=['Qnty'])
    # print(data_forecast)
    dti = pd.date_range('2020-07-14', periods=16)
    data_forecast.set_index(dti, inplace=True)
    data_forecast.index = pd.to_datetime(data_forecast.index)
    old_history.index = pd.to_datetime(old_history.index)
    print("15 DAYS PRED ")
    print(data_forecast)
    data_forecast[data_forecast['Qnty'] < 0] = 0
    return get15DaysPredictionBars(data_forecast)

def getItemPrediction():
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
                                            id='predictionItemDropDown',
                                            options=getItemDropDownItems(),
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

                    dbc.Row(dbc.Col(html.Div(id='predcitionItemTimeLine',
                                             style={'margin-top': '-45px', }), width=12)),

                ], style={
                    # 'margin-bottom': '10px',
                    # 'padding':'10px',
                    'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                    'background-color': 'white',
                    # 'height':'500',
                    # 'width':'100%'
                })
            ], width=12),
        ]),
        dbc.Row([
            html.Div(
                    html.Div(id='itemsPredcitionBars', style={
                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        'background-color': 'white',
                    }), className='mt-3 col-sm-12 col-md-12 col-lg-5 col-xl-5'),
            
            html.Div(
                    html.Div(get15DaysPrediction(), style={
                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        'background-color': 'white',
                    })
                    ,className='mt-3 col-sm-12 col-md-12 col-lg-7 col-xl-7'),
        
        ],className="mt-3")
    
    ]

@app.callback(
    Output("predcitionItemTimeLine", "children"),
    Output("itemsPredcitionBars", "children"),

    [Input("predictionItemDropDown", "value")],
)
def predcitionCustTimeLineFunction(value):
    if value == None:
        value = 7
    return getCustPredictionsGraphs(value)

def getPredictionLayout():
    return html.Div(
        style={'padding': '15px', 'width': '100%',
               'background-color': '#F8FBF6'},
        children=[
            dbc.Tabs(
                [
                    dbc.Tab(label="Item 1077", tab_id=1077),
                    dbc.Tab(label="Item 3411", tab_id=3411),
                    dbc.Tab(label="Item 1616", tab_id=1616),
                    dbc.Tab(label="Item 1086", tab_id=1086),
                    dbc.Tab(label="Item 1852", tab_id=1852),
                ],
                id="item-pred-tabs",
                active_tab=1077,
            ),
            html.Div(id="item-pred-tab-content", className="p-0"),
            #

        ]  # MAIN HTML END,
        , className='container-fluid'
    )

@app.callback(
    Output("item-pred-tab-content", "children"),
    [Input("item-pred-tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab:
        if active_tab == 1077:
            selectedItem.append(1077)
            return getItemPrediction()
        elif active_tab == 3411:
            selectedItem.append(3411)
            return getItemPrediction()
        elif active_tab ==1616 :
            selectedItem.append(1616)
            return getItemPrediction()
        elif active_tab == 1086:
            selectedItem.append(1086)
            return getItemPrediction()
        elif active_tab == 1852:
            selectedItem.append(1852)
            return getItemPrediction()

    return "No tab selected"

