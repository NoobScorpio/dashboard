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
import datetime
from datetime import date, timedelta
from app import app
from dash.dependencies import Input, Output
from . import salesPage as cP
sales = pd.read_csv(
    r'./data/Sells(C).csv')

totalData = pd.read_csv(
    r'./data/compItemCust.csv')
totalData = totalData[totalData['ItemNo'] != '.']
totalData['ItemNo'] = totalData['ItemNo'].astype(int)
totalData['CustomerNo'] = totalData['CustomerNo'].astype(int)
totalData['InvoiceDate'] = pd.to_datetime(totalData['InvoiceDate'])


sales['InvoiceDate'] = pd.to_datetime(sales['InvoiceDate'])
monthNames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors

def getItems():
    items = list(totalData['ItemNo'].unique())
    itemsList = []
    for i in items:
        itemsList.append({'label': i, 'value': i})
    return itemsList


def getCustomers():
    cust = list(totalData['CustomerNo'].unique())
    custList = []
    for i in cust:
        custList.append({'label': i, 'value': i})
    return custList


def getTimeLineGraph(nowData, period):
    nowData['Max'] = max(nowData['Total'])
    fig = go.Figure(
        data=[
            go.Line(
                marker_color="rgb(15,100,84)",
                name='Sales',
                x=nowData.index,
                y=nowData['Total'],
                fill='tozeroy',
                fillcolor='rgba(193, 255, 117, 0.2)',
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),

            go.Line(
                marker_color="grey",
                name='Max',
                x=nowData.index,
                y=nowData['Max'],
                line=dict(color='grey', width=1,
                          dash='dash'),
            ),


        ], )
    fig.update_layout(
        title_text=f'<b>{period} TimeLine</b>',
        xaxis_title="<b>Date</b>",
        yaxis_title="<b>Sales</b>",
        plot_bgcolor='rgba(0, 0, 0, 0)',)

    return dcc.Graph(figure=fig)


def getTimeLineValueBox(title, value):
    return html.Div(
        [
            html.Div(f'{title}', style={
                'margin': '5px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{value}", style={
                'margin': '10px',
                'color': '#89B850',
                'font-size': '24px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ],
        style={
            'margin-top': '10px',
            'height': '100px',
            'width': '95%',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'border': '1px solid #ebebeb', }
    )


def getTimeLineComparison(nSales, nProfit, nQnty, nCusts, pSales, pProfit, pQnty, pCusts, period):
    return [
        dbc.Row(
            dbc.Col([
                html.Div(f'Selected {period}', style={
                    'color': titleColor,
                    'font-size': '22px',
                    "font-weight": "bold",
                }), ], className="mt-3 mr-3 d-flex justify-content-start col-12 col-md-6"
            )),
        dbc.Row(
            [
                dbc.Col(getTimeLineValueBox('Sales', nSales),
                        className="mt-1 d-flex justify-content-center col-12 col-md-6",  ),
                dbc.Col(getTimeLineValueBox('Profit', nProfit),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6", ),
            ]),
        dbc.Row(
            [
                dbc.Col(getTimeLineValueBox('Quantity', nQnty),
                        className="mt-1 d-flex justify-content-center col-12 col-md-6",  ),
                dbc.Col(getTimeLineValueBox('Customers', nCusts),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6", ),
            ]),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(f'Previous {period}', style={
                        'color': titleColor,
                        'font-size': '22px',
                        "font-weight": "bold",
                    }),
                ], className="mt-3 mr-3 d-flex justify-content-start col-12 col-md-6"  
            )),
        dbc.Row(
            [
                dbc.Col(getTimeLineValueBox('Sales', pSales),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6"),
                dbc.Col(getTimeLineValueBox('Profit', pProfit),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6"),
            ]),
        dbc.Row(
            [
                dbc.Col(getTimeLineValueBox('Quantity', pQnty),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6"),
                dbc.Col(getTimeLineValueBox('Customers', pCusts),
                        className="mt-1  d-flex justify-content-center col-12 col-md-6"),
            ]),
    ]


def getGraphAndColumns(nowData, previousData, plotData, period):

    nSales = int(sum(nowData.groupby('InvoiceDate').TotalPrice.sum()))
    nProfit = int(sum(nowData.groupby('InvoiceDate').TotalProfit.sum()))
    nQnty = int(sum(nowData.groupby('InvoiceDate').Qnty.sum()))
    nCusts = len(nowData['InvoiceNo'].unique())
    if previousData.empty:
        pSales = 'N/A'
        pProfit = 'N/A'
        pQnty = 'N/A'
        pCusts = 'N/A'
    else:
        pSales = int(sum(previousData.groupby('InvoiceDate').TotalPrice.sum()))
        pProfit = int(sum(previousData.groupby(
            'InvoiceDate').TotalProfit.sum()))
        pQnty = int(sum(previousData.groupby('InvoiceDate').Qnty.sum()))
        pCusts = len(previousData['InvoiceNo'].unique())

    return getTimeLineGraph(plotData, period), getTimeLineComparison(nSales, nProfit, nQnty, nCusts, pSales, pProfit, pQnty, pCusts, period)


def getTimeLinePlot(period):

    sales['InvoiceDate'] = pd.to_datetime(sales['InvoiceDate'])
    lastDate = sales.tail(1)['InvoiceDate'].item()
    lastDate = pd.to_datetime(lastDate, format='%y-%m-%d')

    totalData['InvoiceDate'] = pd.to_datetime(totalData['InvoiceDate'])
    totalLastDate = totalData.tail(1)['InvoiceDate'].item()
    totalLastDate = pd.to_datetime(totalLastDate, format='%y-%m-%d')

    nowData = totalData

    previousData = totalData

    plotData = sales

    # prevData = None

    if period == 'Max':
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())
        nowData = totalData
        previousData = pd.DataFrame([])

    elif period == '1 Week':

        timeDiff = lastDate-timedelta(7)
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')

        nowData = nowData[nowData['InvoiceDate'] > timeDiff]

        plotData = plotData[plotData['InvoiceDate'] > timeDiff]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())

        # PREV

        timeDiff2 = lastDate-timedelta(14)
        timeDiff2 = pd.to_datetime(timeDiff2, format='%y-%m-%d')

        previousData = previousData[previousData['InvoiceDate'] > timeDiff2]
        previousData = previousData[previousData['InvoiceDate'] < timeDiff]

        # prevData=pd.DataFrame(prevData.groupby('InvoiceDate').Total.sum())

    elif period == '2 Weeks':

        timeDiff = lastDate-timedelta(14)
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')

        nowData = nowData[nowData['InvoiceDate'] > timeDiff]

        plotData = plotData[plotData['InvoiceDate'] > timeDiff]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())

        # PREV
        timeDiff2 = lastDate-timedelta(28)
        timeDiff2 = pd.to_datetime(timeDiff2, format='%y-%m-%d')

        previousData = previousData[previousData['InvoiceDate'] > timeDiff2]
        previousData = previousData[previousData['InvoiceDate'] < timeDiff]
        # prevData=pd.DataFrame(prevData.groupby('InvoiceDate').Total.sum())

    elif period == '1 month':

        timeDiff = lastDate-timedelta(30)
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')

        nowData = nowData[nowData['InvoiceDate'] > timeDiff]

        plotData = plotData[plotData['InvoiceDate'] > timeDiff]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())

        # PREV
        timeDiff2 = lastDate-timedelta(60)
        timeDiff2 = pd.to_datetime(timeDiff2, format='%y-%m-%d')

        previousData = previousData[previousData['InvoiceDate'] > timeDiff2]
        previousData = previousData[previousData['InvoiceDate'] < timeDiff]

        # prevData=pd.DataFrame(prevData.groupby('InvoiceDate').Total.sum())

    elif period == '6 months':

        timeDiff = lastDate-timedelta(int(366/2))
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')

        nowData = nowData[nowData['InvoiceDate'] > timeDiff]

        plotData = plotData[plotData['InvoiceDate'] > timeDiff]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())
        # PREV
        timeDiff2 = lastDate-timedelta(366)
        timeDiff2 = pd.to_datetime(timeDiff2, format='%y-%m-%d')

        previousData = previousData[previousData['InvoiceDate'] > timeDiff2]
        previousData = previousData[previousData['InvoiceDate'] < timeDiff]

        # prevData=pd.DataFrame(prevData.groupby('InvoiceDate').Total.sum())

    elif period == '1 year':

        timeDiff = lastDate-timedelta(364)
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')

        nowData = nowData[nowData['InvoiceDate'] > timeDiff]

        plotData = plotData[plotData['InvoiceDate'] > timeDiff]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())
        # PREV
        timeDiff2 = lastDate-timedelta(364*2)
        timeDiff2 = pd.to_datetime(timeDiff2, format='%y-%m-%d')

        previousData = previousData[previousData['InvoiceDate'] > timeDiff2]
        previousData = previousData[previousData['InvoiceDate'] < timeDiff]

        # prevData=pd.DataFrame(prevData.groupby('InvoiceDate').Total.sum())

    elif period == '5 years':
        nowData = nowData[nowData['Year'] >= max(nowData['Year'])-4]

        plotData = plotData[plotData['Year'] >= max(plotData['Year'])-4]
        plotData = pd.DataFrame(plotData.groupby('InvoiceDate').Total.sum())
        previousData = pd.DataFrame([])

    return getGraphAndColumns(nowData, previousData, plotData, period)


def getSalesTuningRow(item, cust, value):
    selectedData = totalData[totalData['ItemNo'] == int(item)]
    selectedData = selectedData[selectedData['CustomerNo'] == int(cust)]
    # print(selectedData)
    return getManipulatedData(selectedData, value)


def getManipulatedData(data, value):
    selectedData = data
    oldPrice = int(selectedData['Price'].mode())
    newPrice = int(value)
    changedData = selectedData
    # print(changedData)
    changedData['Price'] = value

    changedData['NewPrice'] = value*changedData['Qnty']

    profit = int(sum(
        selectedData['TotalPrice']-selectedData['TotalCost']-selectedData['Discount']))
    sales = int(sum(selectedData['TotalPrice']))
    # print(changedData)
    changedProfit = int(
        sum(changedData['NewPrice']-changedData['TotalCost']-changedData['Discount']))
    changedSales = int(sum(changedData['NewPrice']))
    print(sales, changedSales)
    print(profit, changedProfit)
    if sales == 0:
        percentage = ((changedSales-1)/1)
    else:
        percentage = ((changedSales-sales)/sales)
    graph = getComparisonGraph(list(selectedData['TotalPrice']), list(
        changedData['NewPrice']), list(selectedData['InvoiceDate']))

    return getComparisonValues(sales, profit, changedSales, changedProfit, percentage, oldPrice, newPrice), graph


def getComparisonGraph(original, changed, dates):
    fig = go.Figure(
        data=[
            go.Line(
                marker_color='rgb(135,197,95)',
                name='Original',
                x=dates,
                y=original,

                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },),

            go.Line(
                marker_color='rgb(15,100,84)',
                name='Changed',
                x=dates,
                y=changed,

                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },),
        ])
    fig.update_layout(
        title_text='<b>Values Comparison</b>',
        plot_bgcolor='rgba(0, 0, 0, 0)',
    )
    return dcc.Graph(figure=fig)


def getComparisonValues(sales, profit, cSales, cProfit, percentage, old, new):
    return [
        dbc.Row(
            dbc.Col(
                
                    f'BEFORE CHANGE ( {old} )', style={
                        'color': titleColor,
                        'font-size': '22px',
                        "font-weight": "bold",
                    }
                , className="mt-3 mr-3 d-flex justify-content-start col-12 col-md-6"
            ),
            ),
        dbc.Row(
            [
                dbc.Col(getValueBox('Total Sales', sales),
                        className="mt-3 d-flex justify-content-center col-12 col-md-6"),
                dbc.Col(getValueBox('Profit', profit),
                        className="mt-3  d-flex justify-content-center col-12 col-md-6"),
            ]),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(f'AFTER CHANGE ( {new} )', style={
                        'color':titleColor,
                        'font-size': '22px',
                        "font-weight": "bold",
                    }),
                ], className="mt-3 mr-3 d-flex justify-content-start col-12 col-md-6"
            )),
        dbc.Row(
            [
                dbc.Col(getValueBox('Total Sales', cSales),
                        className="mt-3  d-flex justify-content-center col-12 col-md-6"),
                dbc.Col(getValueBox('Profit', cProfit),
                        className="mt-3  d-flex justify-content-center col-12 col-md-6"),
            ]),
        dbc.Row(
            [
                dbc.Col(getPercentageBox('Percentage Difference', str(round(
                    percentage, 2))), className="mt-3 mb-2 d-flex justify-content-center col-12 col-md-6"),

            ]),
    ]


def getPercentageBox(title, value):
    return html.Div(
        [
            html.Div(f'{title}', style={
                'margin': '15px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{value}", style={
                'margin': '10px',
                'margin-left': '25px',
                'color': '#89B850',
                'font-size': '24px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ],
        style={
            'margin-top': '20px',
            'height': '120px',
            'width': '99%', 'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                            'border': '1px solid #ebebeb', }
    )


def getValueBox(title, value):
    return html.Div(
        [
            html.Div(f'{title}', style={
                'margin': '15px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{value}", style={
                'margin': '10px',
                'color': '#89B850',
                'font-size': '24px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ],
        style={
            'margin-top': '20px',
            'height': '120px',
            'width': '99%',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'border': '1px solid #ebebeb', }
    )


# MAIN

dropDownStyle = {
    'justify-content': 'end',
    'align-content': 'center',    'text-align': 'center',
    'border': '1px solid #89B850',
    'color': '#89B850',
    'appearance': 'none',
    'min-width': '100px',
    'box-shadow': 'none',
    ' font-size': '13px',
}


def salesTimeLine():
    return [
        dbc.Row([

            html.Div(
                [
                    html.Div('Sales Comparison', style={
                        'font-size': '32px',
                        'font-weight': 'bold',
                        'margin-bottom': '10px',
                        'margin-left': '10px',
                    }),
                    dbc.Tabs(
                        [
                            dbc.Tab(label="1 Week",      tab_id="1 Week",),
                            dbc.Tab(label="2 Weeks",     tab_id="2 Weeks",),
                            dbc.Tab(label="1 month",    tab_id="1 month",),
                            dbc.Tab(label="6 months",   tab_id="6 months",),
                            dbc.Tab(label="1 year",     tab_id="1 year",),
                            dbc.Tab(label="5 years",     tab_id="5 years",),
                            dbc.Tab(label="Max",        tab_id="Max",),
                        ],
                        id="timeLineTab",
                        active_tab="1 Week",
                    ),
                    html.Div(id="timeLineTabContent", className="p-4"),
                ],  className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-8"
            ),

            html.Div(id="timeLineTabContentColumn",  className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-4"),

        ]),
    ]

# Main TABS CALLBACK


@app.callback(
    Output("timeLineTabContent", "children"),
    Output("timeLineTabContentColumn", "children"),
    [Input("timeLineTab", "active_tab")],
)
def render_tab_content(active_tab):
    plot, cols = getTimeLinePlot(active_tab)
    return plot, cols


def salesTuning():
    return [
        html.Div(
            [html.Div('Sales Tuning', style={
                'font-size': '32px',
                'font-weight': 'bold',
                'margin-bottom': '10px',
            }),
                dbc.Row([
                    
                    dbc.Col(
                        [
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        'ItemNo',
                                        style={
                                            # 'margin-left':'10px',
                                            'font-size': '24px',
                                            "font-weight": "bold"}
                                    ), className="d-flex justify-content-end"
                                ),
                                dbc.Col(html.Div(
                                    dcc.Dropdown(
                                        id='itemTuneDropdown',
                                        options=getItems(),
                                        value=3,
                                        searchable=False,
                                        style={'width': '150px'}
                                    ), style=dropDownStyle,), className="d-flex justify-content-end")

                            ])
                        ], className="mt-3 mr-5 d-flex justify-content-end", width=3),
                    
                    dbc.Col(
                        [
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        'CustomerNo',
                                        style={
                                            # 'margin-left':'10px',
                                            'font-size': '24px',
                                            "font-weight": "bold"}
                                    ), className="d-flex justify-content-end"
                                ),

                                dbc.Col(html.Div(
                                    dcc.Dropdown(
                                        id='custTuneDropdown',
                                        options=getCustomers(),
                                        searchable=False,
                                        value=1,
                                        style={'width': '150px'}
                                    ), style=dropDownStyle,), className="d-flex justify-content-end")
                            ]),


                        ], className="mt-3 ml-1 mr-5 d-flex justify-content-end", width=3),
                    dbc.Col(
                        [
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        'Value',
                                        style={
                                            'margin-left': '10px',
                                            'font-size': '24px',
                                            "font-weight": "bold"}
                                    ), className="d-flex justify-content-end"
                                ),
                                dbc.Col([html.Div(
                                    [
                                        dbc.Input(id="valueTuneInput", type="number",
                                                  value=50, placeholder="Enter Price of Item")
                                    ], style={
                                        'width': '175px',
                                        'justify-content': 'end',
                                        'align-content': 'center',    'text-align': 'center',
                                    },)], className="d-flex justify-content-end")])

                        ], className="mt-3 ml-1 mr-5 d-flex justify-content-end", width=3),
                ]),

                # GRAPH ROW

                dbc.Row([
                    dbc.Col(id='tuningGraph', width=12, className='p-0')
                ]),
            ], className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-8"
        ),
        # OUTER COLUMN TWO

        html.Div(id='tuningColumn', className="mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-4"),

    ]


# TUNING CALLBACK
@app.callback(
    Output("tuningColumn", "children"),
    Output("tuningGraph", "children"),
    [Input("itemTuneDropdown", "value"), Input(
        "custTuneDropdown", "value"), Input("valueTuneInput", "value"), ],
)
def render_tab_content(itemNo, custNo, value):
    if value == None:
        value = 0
    col, graph = getSalesTuningRow(itemNo, custNo, value)
    return col, graph


def salesAdvancedTab():
    return [
        dbc.Row(

            dbc.Col(
                html.Div(salesTimeLine(), style={
                'margin': '1px',
                # 'padding':'10px',
                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                'background-color': 'white',
                'height': '100%', 'width': '100%'
            }), width=12), className="mt-3"),
        dbc.Row(salesTuning(), style={
            # 'margin': '1px',
            # 'padding':'10px',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'background-color': 'white',
            # ,'height':'100%','width':'99%'
        }, className='mt-3'),
    ]
