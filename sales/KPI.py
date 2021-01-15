from datetime import date
from app import app
import plotly.graph_objects as go
import dash_daq as daq
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from . import salesPage as cP
external_stylesheets = [dbc.themes.BOOTSTRAP]
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

item_details = pd.read_csv(
    r'./data/compItemCust.csv')
item_details = item_details[item_details['ItemNo'] != '.']
item_details['ItemNo'] = item_details['ItemNo'].astype(int)
item_details['Year'] = item_details['Year'].astype(int)
item_details['Month'] = item_details['Month'].astype(int)
item_details['Day'] = item_details['Day'].astype(int)
item_details['CustomerNo'] = item_details['CustomerNo'].astype(int)
item_details['InvoiceDate'] = pd.to_datetime(item_details['InvoiceDate'])

titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
   
def getItemsData():
    return item_details


def getItems():
    items = list(item_details['ItemNo'].unique())
    itemsList = []
    for i in items:
        itemsList.append({'label': i, 'value': i})
    return itemsList


def getCustomers():
    cust = list(item_details['CustomerNo'].unique())
    custList = []
    for i in cust:
        custList.append({'label': i, 'value': i})
    return custList


def getAvgSaleStyle(avgSale):
    return html.Div(f"{avgSale}", style={
        'margin': '10px',
        'margin-top': '60px',
        # 'color':fontCol,
        'color': 'white',
        'font-size': '60px',
        "font-weight": "bold",
        'justify-content': 'center',
        'text-align': 'center'
    })


def getAvgGraph(plot):
    fig = go.Figure(
        data=[
            go.Line(
                marker_color='white',
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=plot.index,
                y=plot['TotalPrice'],
                fill='tozeroy',
                fillcolor='rgba(193, 255, 117, 0.2)',
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            )
        ], )
    fig.update_layout(
        # autosize=False,
        # width=350,
        height=250,
        title_text=f'',
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='#2EB872',
        paper_bgcolor='#2EB872')

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        visible=False,)

    fig.update_yaxes(
        showgrid=False,
        zeroline=False,
        visible=False,)

    return dcc.Graph(figure=fig)


def getAvgItemSalesGraph(itemNo):
    item = item_details[item_details['ItemNo'] == int(itemNo)]

    plot = pd.DataFrame(item.groupby('InvoiceDate').TotalPrice.sum())

    avgSale = round(sum(item['TotalPrice']/sum(item['Qnty'])), 3)

    return getAvgSaleStyle(avgSale), getAvgGraph(plot)


def getAvgCustomerSalesGraph(custNo):
    item = item_details[item_details['CustomerNo'] == int(custNo)]

    plot = pd.DataFrame(item.groupby('InvoiceDate').TotalPrice.sum())

    avgSale = round(sum(item['TotalPrice']/sum(item['Qnty'])), 3)

    return getAvgSaleStyle(avgSale), getAvgGraph(plot)


def getRushHours():
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=270,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Speed"}))
    return dcc.Graph(figure=fig)


def getKPIChurnNumber():
    prevL, nowL = [], []
    for i in yearsName:
        if i != 2020:
            prev = item_details[item_details['Year'] == i]
            now = item_details[item_details['Year'] == i+1]
            prev = list(prev['CustomerNo'].unique())
            now = list(now['CustomerNo'].unique())
            prevL.append(len(prev))
            nowL.append(len(now))
        #
    churn = []
    for i, j in zip(prevL, nowL):
        churn.append((i-j)/i)
    churnRate = 0
    for i in churn:
        churnRate += i
    churnRate = churnRate/len(churn)
    # print(prevL,nowL,churnRate)
    return html.Div(f"{round(churnRate,2)}%", style={
        'margin': '10px',
        'margin-top': '40px',
        # 'color':fontCol,
        'color': 'white',
        'font-size': '72px',
        "font-weight": "bold",
        'justify-content': 'center',
        'text-align': 'center'
    })


def getTargetGauge(sales, customers, items, days):

    df = item_details
    df = df[df['Year'] == max(df['Year'])]
    df = df[df['Month'] == max(df['Month'])]
    # DAY PROGRESS
    daysPassed = len(list(df['Day'].unique()))
    daysProgress = 100-int(((days-daysPassed)/days)*100)
    daysProgress = round((daysProgress*25)/100, 2)
    # SALES PROGRESS
    salesCompleted = int(sum(df['TotalPrice']))
    salesProgress = int(((sales-salesCompleted)/sales)*100)
    if salesProgress < 0:
        salesProgress = 0
    salesProgress = 100-salesProgress
    salesProgress = round((salesProgress*25)/100, 2)
    if salesProgress < 0:
        salesProgress = 0

    # CUSTOMERS PROGRESS
    custProgress = len(list(df['CustomerNo'].unique()))
    # print(f'TOTAL CUSTOMERS CAME : {custProgress}')
    custProgress = int(((customers-custProgress)/customers)*100)
    if custProgress < 0:
        custProgress = 0
    custProgress = 100-custProgress
    # print(f'REMAINING : {custProgress}')
    custProgress = round((custProgress*25)/100, 2)

    # ITEMS PROGRESS
    itemsProgress = int(sum(df['Qnty']))
    itemsProgress = int(((items-itemsProgress)/items)*100)
    if itemsProgress < 0:
        itemsProgress = 0
    itemsProgress = 100-itemsProgress
    itemsProgress = round((itemsProgress*25)/100, 2)
    if itemsProgress < 0:
        itemsProgress = 0
    # print(f'DAYS PROGRESS {daysProgress}')
    # print(f'SALES PROGRESS {salesProgress}')
    # print(f'CUSTOMERS PROGRESS {custProgress}')

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=daysProgress + salesProgress + custProgress + itemsProgress,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Target", 'font': {'size': 24}},
        # delta = {'reference': 400, 'increasing': {'color': "RebeccaPurple"}},
        gauge={
            'axis': {'range': [None, 105], 'tickwidth': 5, 'tickcolor': "skyblue"},
            'bar': {'color': "#2EB872"},
            'bgcolor': "white",
            'borderwidth': 0.5,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, daysProgress], 'color': '#141518'},
                {'range': [25, 25+salesProgress], 'color': '#2E742B'},
                {'range': [50, 50+custProgress], 'color': '#00A000'},
                {'range': [75, 75+itemsProgress], 'color': '#2EB872'},
            ],
            'threshold': {
                'line': {'color': "red", 'width': 2},
                'thickness': 0.5,
                'value': 100}}))

    fig.update_layout(
         autosize=True,
        paper_bgcolor="white", font={'color': "black", 'family': "Arial"})
    return dcc.Graph(figure=fig)


def getItemsSalesDiscountGraph(plot, plotA):
    # print(plot)
    # print(plotA)
    fig = go.Figure(
        data=[
            go.Line(
                marker_color='red',
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=plot.index,
                y=plot['TotalPrice'],
                fill='tozeroy',
                fillcolor='rgba(193, 255, 117, 0.2)',
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),
            go.Line(
                marker_color='blue',
                # "rgba(137, 184, 80, 1)",
                name='Discount Sales',
                x=plotA.index,
                y=plotA['NewTotalPrice'],
                fill='tozeroy',
                fillcolor='rgba(193, 255, 117, 0.2)',
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),
        ], )
    fig.update_layout(
        # autosize=False,
        # width=870,
        height=470,
        title_text=f'',
        xaxis_title="",
        yaxis_title="",
        plot_bgcolor='rgba(0, 0, 0, 0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.5
        )
    )

    return dcc.Graph(figure=fig)


def getItemsSalesDiscount(itemNo, price, dt):
    dt = dt.split('-')

    # dt=date(int(dt[0]),int(dt[1]),int(dt[2]))

    data = item_details[item_details['ItemNo'] == itemNo]
    # print(data)

    dataBefore = data[data['Year'] <= int(dt[0])]
    dataBefore = dataBefore[dataBefore['Month'] <= int(dt[1])]
    dataBefore = dataBefore[dataBefore['Day'] <= int(dt[2])]
    dataBefore = pd.DataFrame(
        dataBefore.groupby('InvoiceDate').TotalPrice.sum())
    print(f"DATA BEFORE MODE")
    print(data)
    # print(f"THIS IS THE YEAR {int(dt[0])}")
    dataAfter = data[data['Year'] == int(dt[0])]
    print('YEAR SELECTE')
    print(dataAfter)
    dataAfter = dataAfter[dataAfter['Month'] == int(dt[1])]
    # print('MONTH SELECTE')
    # print(dataAfter)
    dataAfter = dataAfter[dataAfter['Month'] >= int(dt[1])]
    # print('DAY SELECTE')
    # print(dataAfter)
    dataAfter['NewPrice'] = price

    dataAfter['NewTotalPrice'] = dataAfter['NewPrice']*dataAfter['Qnty']
    # print(dataAfter)

    # print(dataAfter)
    dataAfter = pd.DataFrame(dataAfter.groupby(
        'InvoiceDate').NewTotalPrice.sum())
    return getItemsSalesDiscountGraph(dataBefore, dataAfter)


# MAIN


def getAvgSalesPerItem():
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Average Sales Per Item', style={
                            'margin': '10px',
                            'font-size': '24px',
                            'font-weight': 'bold',
                            'color': 'white',
                        })
                    ], width=7
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id='KPIItemDropdown',
                            options=getItems(),
                            value=3,
                            searchable=False,
                            style={'margin': '10px', 'width': '150px'}
                        )
                    ],
                ),

            ]),

        dbc.Row([
            dbc.Col(
                [

                    html.Div(id='KPIAvgSalePerItem')
                ], width=5
            ),
            dbc.Col(
                id='KPIAvgSalePerItemGraph', width=7
            ),
        ]),
    ]


@app.callback(
    Output("KPIAvgSalePerItem", "children"),
    Output("KPIAvgSalePerItemGraph", "children"),
    [Input("KPIItemDropdown", "value")],
)
def KPIAvgSalePerItemFunction(value):

    return getAvgItemSalesGraph(value)

 
def getAvgSalesPerCustomer():
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Average Sales Per Customer', style={
                            'margin': '10px',
                            'font-size': '24px',
                            'font-weight': 'bold',
                            'color': 'white',
                        })
                    ], width=7
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id='KPICustomerDropdown',
                            options=getCustomers(),
                            value=1,
                            searchable=False,
                            style={'margin': '10px', 'width': '150px'}
                        )
                    ]
                ),

            ]),

        dbc.Row([
            dbc.Col(
                [
                    html.Div(),
                    html.Div(id='KPIAvgSalePerCustomer')
                ], width=5
            ),
            dbc.Col(
                id='KPIAvgSalePerCustomerGraph', width=7
            ),
        ]),
    ]


@app.callback(
    Output("KPIAvgSalePerCustomer", "children"),
    Output("KPIAvgSalePerCustomerGraph", "children"),
    [Input("KPICustomerDropdown", "value")],
)
def KPIAvgSalePerCustomerFunction(value):

    return getAvgCustomerSalesGraph(value)


def getKPIItemDiscountSales():
    return [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div('Item Dicount Sale Timeline', style={
                            'margin': '25px',
                            'font-size': '30px',
                            'font-weight': 'bold',
                            'color': titleColor,
                        })
                    ]
                ),

            ]),
        dbc.Row([
            dbc.Col(
                [

                    html.Div(
                        'Select Item',
                        style={
                            'margin-left': '20px',
                            'font-size': '24px',
                            'color':fontCol,
                            "font-weight": "bold"}
                    ),
                    dcc.Dropdown(
                        id='KPIItemSalesDiscountDropdown',
                        options=getItems(),
                        value=3,
                        searchable=False,
                        style={'margin': '10px', 'width': '150px'}
                    ),

                ]
            ),
            dbc.Col(
                [

                    html.Div(
                        'Enter Discount Price',
                        style={
                            'margin-bottom': '10px',
                            'font-size': '24px',
                            'color':fontCol,
                            "font-weight": "bold"}
                    ),
                    html.Div(
                        dbc.Input(id="KPIItemSalesDiscountInput", type="number", value=250, placeholder="Enter Price "), style={
                            'width': '200px'
                        })

                ]
            ),
        ],className="d-flex justify-content-start"),

        dbc.Row([

            html.Div(
                'Select Date',
                style={
                    'margin-right': '20px',
                    'margin-left': '5px',
                    'margin-top': '5px',
                    'color':fontCol,
                    'font-size': '24px',
                    "font-weight": "bold"}
            ),
            html.Div(dcc.DatePickerSingle(
                id='datePicker',
                initial_visible_month=date(2020, 1, 7),
                date=date(2020, 7, 7),
                display_format='Y-M-D'
            ))
        ], className='d-flex ml-3 mt-3'),

        dbc.Row([
            dbc.Col(
                [

                    html.Div(id='KPIItemSalesDiscountGraph')
                ], 
            ),
        ]),
    ]


@app.callback(
    Output("KPIItemSalesDiscountGraph", "children"),
    [Input("KPIItemSalesDiscountDropdown", "value"),
     Input("KPIItemSalesDiscountInput", "value"),
     Input("datePicker", "date"), ],
)
def KPIItemSalesDiscountInputFunction(value, value2, value3):
    if value2 == None:
        value2 = 0
    # print(f"THIS IS INPUT VALUE {value3}")
    return getItemsSalesDiscount(value, value2, value3)


def KPIChurnNumber():
    return dbc.Col([
        html.Div('Churn Rate', style={
            'margin': '10px',
            
            'font-size': '32px',
            'font-weight': 'bold',
            'color': 'white',
        }),
        getKPIChurnNumber(),
    ], width=12),


def getKPISellMenData(target):
    data = getItemsData()
    returnData = [
    ]
    i = 0
    for sellMan in data["SellManNo"].unique():
        selectedData = data[data['SellManNo'] == sellMan]
        profit = round(sum(pd.DataFrame(selectedData.groupby(
            'SellManNo').TotalProfit.sum())['TotalProfit']), 2)

        qnty = round(
            sum(pd.DataFrame(selectedData.groupby('SellManNo').Qnty.sum())['Qnty']), 2)
        # print(f"TARGET IN FUNC {target}")
        progress = int(((target-profit)/target)*100)
        if progress > 100:
            progress = 100
        if progress < 0:
            progress = 0
        # print(f"PROGRESS {progress}")
        returnData.append(
            dbc.Row(
                dbc.Col(html.Div([

                    dbc.Row([
                        dbc.Col([
                            html.Div(f'Sell Man {sellMan}', style={
                                'margin': '10px',
                                'font-size': '24px',
                                'font-weight': 'bold',
                                'color': fontCol,
                            })
                        ], width=4),

                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div(f'Profit Generated', style={
                                'margin': '10px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': 'black',
                            })
                        ], width=6),
                        dbc.Col([

                            html.Div(f"{profit}", style={
                                'margin': '10px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': fontCol,
                            })
                        ], width=6),
                    ]),

                    dbc.Row([
                        dbc.Col([

                            html.Div(f'Items Sold', style={
                                'margin': '10px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': 'black',
                            }),
                        ], width=6),
                        dbc.Col([
                            html.Div(f"{qnty}", style={
                                'margin': '10px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': fontCol,
                            })
                        ], width=6),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div(f'Target', style={
                                'margin': '10px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': 'black',
                            }),
                        ], width=2),
                        dbc.Col([

                            html.Div(dbc.Progress(value=progress, color="success"), style={
                                'margin': '10px',
                                'margin-top': '20px',
                                'font-size': '20px',
                                'font-weight': 'bold',
                                'color': '#2EB872',
                            }),
                        ], width=10),
                    ]),


                ], style={'margin': '10px',
                          'margin-top': '35px', }), width=12),
            ),
        )
        i += 1
    return [returnData]


def getRushHourGuage():
    base_chart = {
        "values": [40, 10, 10, 10, 10, 10, 10],
        "labels": ["-", "0", "20", "40", "60", "80", "100"],
        "domain": {"x": [0, .48]},
        "marker": {
            "colors": [
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)',
                'rgb(255, 255, 255)'
            ],
            "line": {
                "width": 1
            }
        },
        "name": "Gauge",
        "hole": .4,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 108,
        "showlegend": False,
        "hoverinfo": "none",
        "textinfo": "label",
        "textposition": "outside"
    }
    meter_chart = {
        "values": [50, 10, 10, 10, 10, 10],
        "labels": ["7-9", "9-11", "11-1", "1-3", "3-5"],
        "marker": {
            'colors': [
                'rgb(255, 255, 255)',
                'rgb(232,226,202)',
                'rgb(226,210,172)',
                'rgb(223,189,139)',
                'rgb(223,162,103)',
                'rgb(226,126,64)'
            ]
        },
        "domain": {"x": [0, 0.48]},
        "name": "Gauge",
        "hole": .3,
        "type": "pie",
        "direction": "clockwise",
        "rotation": 90,
        "showlegend": False,
        "textinfo": "label",
        "textposition": "inside",
        "hoverinfo": "none"
    }
    layout = {
        # "width": 800,
        # "height": 800,
        'xaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'yaxis': {
            'showticklabels': False,
            'showgrid': False,
            'zeroline': False,
        },
        'shapes': [
            {
                'type': 'path',
                'path': 'M 0.235 0.5 L 0.24 0.65 L 0.245 0.5 Z',
                'fillcolor': 'rgba(44, 160, 101, 0.5)',
                'line': {
                    'width': 0.5
                },
                'xref': 'paper',
                'yref': 'paper'
            }
        ],
        'annotations': [
            {
                'xref': 'paper',
                'yref': 'paper',
                'x': 0.23,
                'y': 0.45,
                'text': '50',
                'showarrow': False
            }
        ]
    }
    base_chart['marker']['line']['width'] = 0
    fig = {"data": [base_chart, meter_chart],
           "layout": layout}
    return dcc.Graph(figure=fig)


def getKPI():
    return [

        dbc.Row(
            [
                # LEFT COL

                dbc.Col([

                    # FIRST ROW OF FIRST COL
                    dbc.Row(
                        dbc.Col(html.Div(getAvgSalesPerItem()),style={
                            'margin': '10px',
                            # 'padding':'10px',
                            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                            'background': '#2EB872',
                            # 'height':'500',
                            'width': '100%'
                        })
                    ),

                    # SECOND ROW OF FIRST COL

                    dbc.Row(
                        html.Div(getAvgSalesPerCustomer(), style={
                            'margin': '10px',
                            # 'padding':'10px',
                            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                            'background': '#2EB872',
                            # 'height':'100%',
                            'width': '100%'
                        })
                        ),

                    dbc.Row(
                            html.Div(KPIChurnNumber(), style={
                                'margin': '10px',
                                # 'padding':'10px',
                                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                                'background': '#2EB872',
                                # 'height':'500',
                                'width': '100%',
                                'height': '320px',
                                'color': "white !important",
                            })
                        ),

                    ],className="mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-4"),


                # MIDDLE COL

                dbc.Col(
                    [
                        # FIRST COL OF MIDDLE COL
                        dbc.Row(
                            dbc.Col(
                            [
                                dbc.Row(dbc.Col(html.Div('Target Tracker', style={
                                                'font-size': '30px',
                                                'font-weight': 'bold',
                                                'color': titleColor,
                                            }),className="d-flex justify-content-start",style={'margin':'25px'}),),
                                dbc.Row([
                                    dbc.Col(html.Div('Sales Target', style={
                                                'font-size': '22px',
                                                'font-weight': 'bold',
                                                'color': fontCol,
                                            }),className="d-flex justify-content-start",style={'margin':'25px'}),
                                    dbc.Col(html.Div('Customer No', style={
                                                'font-size': '22px',
                                                'font-weight': 'bold',
                                                'color': fontCol,
                                            }),className="d-flex justify-content-start",style={'margin':'25px'}),
                                ]),
                                 dbc.Row([
                                    dbc.Col(dbc.Input(id="salesTargetInput", type="number", value=250000, placeholder="Enter Target"),className="d-flex justify-content-start",style={'margin':'25px','margin-top': '-15px',}),
                                    dbc.Col(dbc.Input(id="custTargetInput", type="number", value=50, placeholder="Enter Target"),className="d-flex justify-content-start",style={'margin':'25px','margin-top': '-15px',}),
                                ]),

                                 dbc.Row([
                                    dbc.Col(html.Div('Items Quantity', style={
                                        'font-size': '22px',
                                        'font-weight': 'bold',
                                        'color': fontCol,
                                    }),className="d-flex justify-content-start",style={'margin':'25px','margin-top': '-15px',}),
                                    dbc.Col(html.Div('Target Time', style={
                                        'font-size': '22px',
                                        'font-weight': 'bold',
                                        'color': fontCol,
                                    }),className="d-flex justify-content-start",style={'margin':'25px','margin-top': '-15px',}),
                                ]),

                                 dbc.Row([
                                    dbc.Col(dbc.Input(id="itemTargetInput", type="number", 
                                    value=6000, placeholder="Enter Target"),
                                    className="d-flex justify-content-start",
                                    style={'margin':'25px','margin-top': '-15px',}),
                                   
                                   dbc.Col(html.Div(dcc.Dropdown(id='targetMonthDropdown', options=[
                                            {'label': '30 Days', 'value': 30},
                                            {'label': '60 Days', 'value': 60},
                                            {'label': '90 Days', 'value': 90}
                                        ], value=30),style={'width':'150px'}),
                                        className="d-flex justify-content-start",
                                        style={'margin':'25px','margin-top': '-15px',}),
                                ]),

                               dbc.Row(dbc.Col(id='targetGuage'))
                            
                            
                            ],style={
                                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                                'background': 'white',
                            }
                            ),
                        ),

                        # SECOND ROW OF MIDDLE COL

                        dbc.Row(
                            dbc.Col(getKPIItemDiscountSales()), style={
                                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                                'background': 'white',
                            },className="mt-3 px-0"
                        ),

                    ],className="mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-4"),



                # RIGHT COL

                html.Div(
                    [
                        

                        # SECOND ROW OF FIRST COL

                        dbc.Row(
                            dbc.Col([
                                dbc.Row(
                                    [dbc.Col(html.Div('SellMen Data', style={
                                        'font-size': '30px',
                                        'font-weight': 'bold',
                                        'color': titleColor,
                                    }),),
                                        dbc.Col([
                                            html.Div('Set Target', style={
                                                'font-size': '22px',
                                                'font-weight': 'bold',
                                                'color': fontCol,
                                                'margin-bottom': '5px',
                                            }),
                                            dbc.Input(id="sellMenTargetInput", type="number",
                                                      value=25000000, placeholder="Enter Target")
                                        ])
                                    ],style={
                                        'margin-top': '15px',
                                    }
                                ),
                                
                                dbc.Row(
                                    dbc.Col(id='sellManDataInput', width=12))
                            
                            ]), style={
                                'margin-left': '5px',
                                # 'padding':'10px',
                                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                                'background': 'white',
                                'height': '100%', 'width': '100%'
                            }
                        ),

                    ],className="mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-4"),

            ]),
    ]


@app.callback(
    [Output("targetGuage", "children")],
    [Input("salesTargetInput", "value"), Input("custTargetInput", "value"), Input(
        "itemTargetInput", "value"), Input("targetMonthDropdown", "value"), ],
)
def targetGuageCallback(sales, customers, items, days):
    if sales == 0:
        sales = 250000
    if customers == 0:
        customers = 50
    if items == 0:
        items = 6000
    if days == 0:
        days = 30
    # print(f"TARGET {target}")
    return [getTargetGauge(sales, customers, items, days)]


@app.callback(
    [Output("sellManDataInput", "children")],
    [Input("sellMenTargetInput", "value")],
)
def update_progress(target):
    # print(f"TARGET {target}")
    return getKPISellMenData(target)
