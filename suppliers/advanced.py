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
from _datetime import timedelta

data = cP.getData()
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

selectedYear = [2020]
selectedMonth=[0]
selectedSupplier=[1]


dropDownStyle = {
    'margin-top': '25px',
    'margin-right': '25px',
    'justify-content': 'end',
    'min-width': '200px',
    'box-shadow': 'none',
    'font-size': '13px',
    'margin-left': '50px',
}

def getYears():
    i = 0
    menuItems = []
    while i < len(yearsName):
        year = yearsName[i]
        menuItems.append({'label': year, 'value': year})
        i += 1

    return menuItems

def getSups():
    i = 0
    menuItems = []
    while i < len(yearsName):
        year = yearsName[i]
        menuItems.append({'label': i, 'value': i})
        i += 1

    return menuItems


def getMonths():
    df=data[data['Year']==selectedYear[-1]]
    months=list(df['Month'].unique())
    print(f" MONTHS : {months}")
    j=0
    menuItems = []
    menuItems.append({'label': "All", 'value': 0})
    for i in months:
        menuItems.append({'label': monthNames[i-1], 'value': i})


    return menuItems


def getFirstRowLayout():
    fig=go.Figure(data=[
        go.Line(
            y=[1000,2000,1500,500,1000],
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
        title_text=f'<b>Supplied Quantity ( {monthNames[selectedMonth[-1]]}, {selectedYear[-1]}, S {selectedSupplier[-1]} )</b>',
        title_font_size=20,
        height=550,
        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    fig2 = go.Figure(
        data=[
            go.Pie(

                labels=['Quantity Order','Received','Defects','Returned'],
                values=[10000,9000,1000,2000],
                # hole=.5,
                marker_colors=colors

            )
        ],
        
    )
    fig2.update_layout(
        height=550,
        title=f'<b>Supplied Quantity Details ( {monthNames[selectedMonth[-1]]}, {selectedYear[-1]}, S {selectedSupplier[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,

    )

    return [
        html.Div(dcc.Graph(figure=fig), className="mt-2 col-sm-12 col-md-12 col-lg-8"),
        html.Div(dcc.Graph(figure=fig2), className="mt-2 col-sm-12 col-md-12 col-lg-4")
    ]

# MAIN CALLBACK
@app.callback(
    Output("supAdvYearMonthDropDownDiv", "children"),
    [Input("supAdvYearDropDown", "value"),],
)
def render_tab_content(value):
    if value==None:
        value=2020
    selectedYear.append(value)
    print("Year APPENDIND ")
    return dcc.Dropdown(
                    id='supAdvYearMonthDropDown', 
                    searchable=False, 
                    options=getMonths(), 
                    value=selectedMonth[-1], 
                    style={
                        'margin-top': '25px',
                        'margin-left': '15px',
                        'margin': '10px',
                        'width': '250px',
                    }
                )

@app.callback(
    Output("supAdvYearMonthNoDiv", "children"),
    [Input("supAdvYearMonthDropDown", "value")])
def itemMonthDropFUnction(value):
    if value == None:
        value = 1
    return dcc.Dropdown(
                    id='supAdvYearMonthNo', 
                    searchable=False, 
                    options=getSups(), 
                    value=selectedSupplier[-1], 
                    style={
                        'margin-top': '25px',
                        'margin-left': '15px',
                        'margin': '10px',
                        'width': '250px',
                    }
                )
@app.callback(
    Output("supAdvFirstRowLayout", "children"),
    [Input("supAdvYearMonthNo", "value")])
def itemMonthSupDropFUnction(value):
    if value == None:
        value = 0
    selectedSupplier.append(value)
    return  getFirstRowLayout()

def getAdvancedLayout():
    return [
    # SELECT YEAR MONTH SUPPLIER ROW
        dbc.Row(
            [
                html.Div([html.Div('Select Year', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                    }),
                        dcc.Dropdown(
                        id='supAdvYearDropDown', searchable=False, options=getYears(), value=2020, style={
                            'margin': '10px',
                            'width': '250px',
                        }
                    )],className="col-4"),

                html.Div([html.Div('Select Month', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                    }),
                    html.Div(id='supAdvYearMonthDropDownDiv', style={
                        'margin': '10px',
                        'width': '250px',
                    }
                     )],className="col-4"),
                
                html.Div([html.Div('Select Supplier', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                    }),
                    html.Div(id='supAdvYearMonthNoDiv', style={
                        'margin': '10px',
                        'width': '250px',
                    })],className="col-4"),




                
            ]),
    
    #  FIRST ROW
    dbc.Row(
        id='supAdvFirstRowLayout'
       
    ),
    # SECOND ROW
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
                        id="suptimeLineTab",
                        active_tab="Max",
                    ),

                    dbc.Row(id='supSalesQuantityTimeLine'),
                    
                    ]
                    ) ),
    
    ]

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
        title_text=f'<b>Supplier No {selectedSupplier[-1]} TimeLine</b>',
        title_font_size=24,
        title_font_color=titleColor,
        # bargap=0.15, # gap between bars of adjacent location coordinates.
        # bargroupgap=0.1, # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=fig)

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
    sales = round(sum(df.groupby('InvoiceDate').TotalPrice.sum()), 2)
    qnty = round(sum(df.groupby('InvoiceDate').Qnty.sum()), 2)
    profit = round(sum(df.groupby('InvoiceDate').TotalProfit.sum()), 2)
    sales, qnty, profit, maxMonth
    return [
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Quantity Ordered', sales), width=6),
            dbc.Col(getTimeLineValueBox('Quantity Received', qnty), width=6),
        ]),
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Quantity Defects', "17856"), width=6),
            dbc.Col(getTimeLineValueBox('Quantity returned', "20400"), width=6),
        ]),
        dbc.Row([
            dbc.Col(getTimeLineValueBox('Supplier Average Response Time', "1 Day"), width=12),
        ]),
    ]
def getTimeLineValueBox(title, value):
    return html.Div(
        [
            html.Div(f'{title}', style={
                'color': 'rgb(55, 83, 109)',
                'margin': '5px',
                'font-size': '24px',
                'color':titleColor,
                "font-weight": "bold"}),

            html.Div(f"{value}", style={
                'margin': '10px',
                'color': fontCol,
                'font-size': '24px',
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

def getSalesQuantityTimeLine(supNo,period):
    df = data

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
        html.Div(getSalesQuantityTimeLineGraph(sales, qnty), className="mt-2 col-sm-12 col-md-12 col-lg-8"),
        html.Div(getSalesQuantityTimeLineComponents(df), className="mt-2 col-sm-12 col-md-12 col-lg-4")
    ]


@app.callback(
    Output("supSalesQuantityTimeLine", "children"),
    [Input("supAdvYearMonthNo", "value"),Input("suptimeLineTab", "active_tab")]
)
def render_tab_content(value,value2):
    if value == None:
        value = 1
    selectedSupplier.append(value)
    return getSalesQuantityTimeLine(value,value2)
    