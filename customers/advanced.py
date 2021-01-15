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
from datetime import date, timedelta
from dash.dependencies import Input, Output
from . import customersPage as cP
data = cP.getData()

titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
# print('ORIGNAL DATA')
# print(data['CustomerNo'])

selectedCustomer = [1]
selectedCustomerItem = [1]
selectedItem = []

monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]


def getCustomers():
    df = data
    custs = list(df['CustomerNo'].unique())
    menuItems = []
    for cust in custs:
        menuItems.append({'label': cust, 'value': cust})
    return menuItems


def getCustomersItems(df):
    items = list(df['ItemNo'].unique())
    menuItems = []
    for cust in items:
        menuItems.append({'label': cust, 'value': cust})
    return menuItems


def getSalesQuantityTimeLineGraph(sales, qnty):
    sales['Max'] = max(sales['TotalPrice'])
    qnty['Max'] = max(qnty['Qnty'])
    fig = go.Figure(
        data=[
            go.Line(
                x=sales.index,
                y=sales['Max'],
                line=dict(color='grey', width=1,
                          dash='dash'),
                name='Max Sales',
            ),
            go.Line(
                x=qnty.index,
                y=qnty['Max'],
                line=dict(color='lightgrey', width=1,
                          dash='dash'),
                name='Max Quantity',
            ),
            go.Line(
                x=sales.index,
                y=sales['TotalPrice'],
                marker_color=fontColDark,
                name='Sales/10',
                line=dict(shape='spline', smoothing=1),
            ),
            go.Line(
                x=qnty.index,
                y=qnty['Qnty'],
                marker_color=fontCol,
                name='Quantity',
                line=dict(shape='spline', smoothing=1),
            )
        ],
        layout=go.Layout(
            xaxis=dict(
                title='<b>Date</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Value</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        )
    )
    fig.update_layout(
        title_text=f'<b>Customers No {selectedCustomer[-1]} TimeLine</b>',
        title_font_size=24,
        title_font_color=titleColor,
        # bargap=0.15, # gap between bars of adjacent location coordinates.
        # bargroupgap=0.1, # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=fig)


def getCustomerItemsGraph(itemNo):
    df = data[data['CustomerNo'] == selectedCustomerItem[-1]]
    df = df[df['ItemNo'] == itemNo]

    demand=df.groupby('InvoiceDate').TotalPrice.sum()
    demand=str(demand[demand==max(demand)].index[0]).split(' ')[0].split('-')
    m=int(demand[1])
    y=int(demand[0])
    demand=F"{monthNames[m-1]}, {y}"
    print(demand)
    
    sales = round(sum(df.groupby('InvoiceDate').TotalPrice.sum()), 2)
    qnty = round(sum(df.groupby('InvoiceDate').Qnty.sum()), 2)
    profit = round(sum(df.groupby('InvoiceDate').TotalProfit.sum()), 2)
    cost = round(df['Cost'].mean(), 2)

    # print(f"THIS IS THE COST {cost}")
    items = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    items['Max'] = max(items['Qnty'])
    # print(df)
    fig = go.Figure(
        data=[
            go.Line(
                x=items.index,
                y=items['Max'],
                line=dict(color='grey', width=1,
                          dash='dash'),
                name='Max',
            ),
            go.Line(
                x=items.index,
                y=items['Qnty'],
                marker_color=fontCol,
                name='Sales/10',
                line=dict(shape='spline', smoothing=1),
            ),
        ],
        layout=go.Layout(
            xaxis=dict(
                title='<b>Date</b>',
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
        )
    )
    fig.update_layout(
        title_text=f'<b>Item No {itemNo} TimeLine</b>',
        title_font_size=24,
        title_font_color=titleColor,
        # bargap=0.15, # gap between bars of adjacent location coordinates.
        # bargroupgap=0.1, # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return [
        html.Div(dcc.Graph(figure=fig),className="mt-2 col-sm-12 col-md-12 col-lg-7 col-xl-8"),
        
        html.Div(
            [

                dbc.Row([
                    dbc.Col(getTimeLineValueBox('Sales', sales), width=6),
                    dbc.Col(getTimeLineValueBox('Quantity', qnty), width=6),
                ]),
                dbc.Row([
                    dbc.Col(getTimeLineValueBox('Profit', profit), width=6),
                    dbc.Col(getTimeLineValueBox('Item Cost', cost), width=6),
                ]),
                dbc.Row([
                    dbc.Col(getTimeLineValueBox('Most Demand Period', demand), width=12),
                ]),

            ],className="mt-2 col-sm-12 col-md-12 col-lg-5 col-xl-4")
    ]


def getCustomerItemsDropDown(custNo):
    df = data[data['CustomerNo'] == custNo]
    itemsList = getCustomersItems(df)
    return [
        dcc.Dropdown(
            id='customersItemDropDown', searchable=False, options=itemsList, value=itemsList[0]['value'], style={
                'margin': '10px',
                'margin-top': '20px',
                'width': '250px',
            }
        )
    ]


def getTimeLineValueBox(title, value):
    # print(f"THE TYPE OF VALUE IS {type(value)}")
    if(type(value)==int or type(value)==float ):
        valint=int(value)
        val=str(value)
        if valint>10000 and valint<100000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
        elif valint>100000 and valint<1000000:
            val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
        elif valint>=1000000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    else:
        val=value
    return html.Div(
        [
            html.Div(f'{title}', style={
                'color': 'rgb(55, 83, 109)',
                'margin': '5px',
                'font-size': '24px',
                'color':titleColor,
                "font-weight": "bold"}),

            html.Div(f"{val}", style={
                'margin': '10px',
                'color': fontCol,
                'font-size': '32px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ],
        style={
            'padding': '10px',
            'margin-top': '10px',
            'height': '150px',
            'background-color': bgCol,
            # 'width':'95%',
            # 'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            # 'border': '1px solid #ebebeb',
        }
    )


def getSalesQuantityTimeLineComponents(df):
    
    pStart=list(df['InvoiceDate'])
    pStart=str(pStart[0]).split(' ')[0]
    # print(pStart)
    pStart=pStart.split('-')
    m=int(pStart[1])
    y=int(pStart[0])
    pStart=F"{monthNames[m-1]}, {y}"

    pEnd=df.tail(1)
    pEnd=str(pEnd['InvoiceDate']).split(' ')[3].split('\n')[0].split('-')
    m=int(pEnd[1])
    y=int(pEnd[0])
    pEnd=F"{monthNames[m-1]}, {y}"
    
    period=f"{pStart} - {pEnd}"
    # print(period)


    
    maxMonth = str(pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum(
    )).idxmax()).split(' ')[3].split('\\')[0].split('-')
    month = int(maxMonth[1])-1
    year = int(maxMonth[0])
    maxMonth = f"{monthNames[month]}, {year}"
    # print(f"MONTHG MAX IS {maxMonth}")
    sales = sum(df.groupby('InvoiceDate').TotalPrice.sum())
    qnty = sum(df.groupby('InvoiceDate').Qnty.sum())
    profit = sum(df.groupby('InvoiceDate').TotalProfit.sum())
    # sales, qnty, profit, maxMonth
    return [
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Sales', sales), width=6),
            dbc.Col(getTimeLineValueBox('Quantity', qnty), width=6),
        ]),
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Profit', profit), width=6),
            dbc.Col(getTimeLineValueBox('Best Month', maxMonth), width=6),
        ]),
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Customer Time Period', period), width=12),
        ]),
    ]


def getSalesQuantityTimeLine(custNo,period):
#     "1 Week" 
# "2 Weeks"
# "1 month"
# "6 months
# "1 year" 
# "5 years"
# "Max"    
    
    df = data[data['CustomerNo'] == custNo]

    lastDate = df.tail(1)['InvoiceDate'].item()
    lastDate = pd.to_datetime(lastDate, format='%y-%m-%d')

    if period=='Max':
        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    
    elif period=='5 years':
        df=df[df['Year']>max(df['Year'])-5]
        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    
    elif period=='1 year':
        df=df[df['Year']>max(df['Year'])-1]
        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    
    elif period=='6 months':
        df=df[df['Year']==max(df['Year'])]
        df=df[df['Month']>max(df['Month'])-5]
        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())

    elif period=='1 month':
        df=df[df['Year']==max(df['Year'])]
        df=df[df['Month']>max(df['Month'])-1]
        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    
    elif period=='2 Weeks':
        
        df=df[df['Year']==max(df['Year'])]
        df=df[df['Month']==max(df['Month'])]
        
        timeDiff = lastDate-timedelta(14)   
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')
        
        df = df[df['InvoiceDate'] > timeDiff]
        
        

        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())
    
    elif period=='1 Week':
        
        df=df[df['Year']==max(df['Year'])]
        df=df[df['Month']==max(df['Month'])]
        
        timeDiff = lastDate-timedelta(7)
        timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')
        
        df = df[df['InvoiceDate'] > timeDiff]
        
        

        sales = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
        sales['TotalPrice'] = sales['TotalPrice']/10
        qnty = pd.DataFrame(df.groupby('InvoiceDate').Qnty.sum())

    return [
        html.Div(getSalesQuantityTimeLineGraph(sales, qnty),className="mt-2 col-sm-12 col-md-12 col-lg-7 col-xl-8"),
        html.Div(getSalesQuantityTimeLineComponents(df),className="mt-2 col-sm-12 col-md-12 col-lg-5 col-xl-4")
    ]


def getCustomersBusinessAndIndividul():
    labels = ['Bussiness Customers', 'Individual Customers']
    values = [2500, 1053, ]
    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=[fontColDark, fontCol, ],),
        ],
        
        )

    fig.update_layout(
        # height=500,
        title=f'<b>Bussiness and Individual Customers</b>',
        title_font_size=20,
        title_font_color=titleColor,
        showlegend=False
    )
    return dcc.Graph(figure=fig)


def getAdvancedLayout():
    return [
        # MAIN ROW
        dbc.Row(
            # MAIN COL
            dbc.Col(
                [

                    # SELECT CUSTOMER ROW
                    dbc.Row(dbc.Col([
                        dbc.Row(
                        [
                            html.Div('Select Customer', style={
                                'margin': '15px',
                                'font-size': '22px',
                                'font-weight': 'bold',
                                'color':titleColor,
                            }),
                            dcc.Dropdown(
                                id='customersDropDown', searchable=False, options=getCustomers(), value=1, style={
                                    'margin': '10px',
                                    'width': '250px',
                                     'color':titleColor,
                                }
                            ),
                        ], className='d-flex justify-content-center'
                    ),

                    # TIMELINE ROW
                   
                    dbc.Row(dbc.Col(
                        [
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
                        id="custtimeLineTab",
                        active_tab="Max",
                    ),
                    dbc.Row(id='customerSalesQuantityTimeLineCust'),
                    ]
                    ) ),
                    

                    ],width=12,style={'background-color':'white'}),className='mt-2 '),

                    # SELECT CUSTOMER ITEM ROW
                    dbc.Row(dbc.Col([
                        dbc.Row(
                        [
                            html.Div('Select Customer', style={
                                'margin': '15px',
                                'font-size': '22px',
                                'font-weight': 'bold',
                                 'color':titleColor,
                            }),
                            dcc.Dropdown(
                                id='customersDropDown2', searchable=False, options=getCustomers(), value=1, style={
                                    'margin': '10px',
                                    'width': '250px',
                                     'color':titleColor,
                                }
                            ),
                            html.Div('Select Item', style={
                                'margin': '15px',
                                'margin-top': '20px',
                                'margin-left': '25px',
                                'font-size': '22px',
                                'font-weight': 'bold',
                                 'color':titleColor,
                            }),
                            html.Div(id='customersItemDropDownArea',),

                        ], className='d-flex justify-content-center'
                    ),

                    # CUSTOMER AND ITEMS TIMELINE
                    dbc.Row(id='itemTimelineGraph'),    

                    ],width=12,style={'background-color':'white'}),className='mt-2 '),
                    # COMPANY INDIVIDUAL
                    dbc.Row(
                        dbc.Col(getCustomersBusinessAndIndividul(), width=12,
                                className='d-flex justify-content-start mt-2')
                    ),

                ], width=12
            )
        ),
    ]



# CUSTEOMRE ITEM CALLBACK
@app.callback(
    Output("customersItemDropDownArea", "children"),
    [Input("customersDropDown2", "value")],
)
def customersDropDown2(value):
    if value == None:
        value = 1
    selectedCustomerItem.append(value)
    # 10443
    # selectedCustomer.append(value)
    return getCustomerItemsDropDown(value)

# ITEMS DROPDOWN


@app.callback(
    Output("itemTimelineGraph", "children"),
    [Input("customersItemDropDown", "value")],
)
def customersDropDownItems(value):
    if value == None:
        value = 10443
    return getCustomerItemsGraph(value)

# MAIN CALLBACK


@app.callback(
    Output("customerSalesQuantityTimeLineCust", "children"),
    [Input("customersDropDown", "value"),Input("custtimeLineTab", "active_tab")],
)
def render_tab_content(value,value2):
    if value == None:
        value = 1
    selectedCustomer.append(value)
    return getSalesQuantityTimeLine(value,value2)

