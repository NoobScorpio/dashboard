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
from . import customersPage as cP
import charts
data = cP.getData()
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
topCustChartType='bar'
custDc = pd.read_csv(
    r'./data/custDebitCredit.csv')


selectedYear = [2020]
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

def getYears():
    i = 0
    menuItems = []
    while i < len(yearsName):
        year = yearsName[i]
        menuItems.append({'label': year, 'value': year})
        i += 1

    return menuItems

def getQuarterlyChart(quarters):
    j = 1
    labels = []
    values = []
    for i in quarters:

        labels.append(f"Quarter {j}")

        values.append(int(i))
        j += 1

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(
        data=[
            go.Pie(

                labels=labels,
                values=values,
                hole=.5,
                marker_colors=colors

            )
        ]
    )
    fig.update_layout(
        # height=550,
        title=f'<b>Total Customers Quarterly ( {selectedYear[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,
        autosize=True,
        

    )
    fig.update_traces(textposition='inside', textfont_size=18)
    return dcc.Graph(figure=fig)

def totalCustomersPerYear(year,hole):
    df = data
    df = df[df['Year'] == year]
    quarters = [g for n, g in df.groupby(
        pd.Grouper(key='InvoiceDate', freq='Q'))]
    # print(quarters)
    custs_list = []
    for i in quarters:
        custs_list.append(len(i['CustomerNo'].unique()))
    custs = len(df['CustomerNo'].unique())
    # print(custs_list)
    # print(custs)
    j = 1
    labels = []
    values = []
    for i in custs_list:
        labels.append(f"Quarter {j}")
        values.append(int(i))
        j += 1
    return html.Div(
        [dbc.Row(
            
               
                    html.Div(f'Total Customers ( {selectedYear[-1]} )', style={

                        'font-size': '28px',
                        'font-weight': 'bold',
                        'margin': '10px',
                        'color': titleColor,
            })
            
            
        ),
        dbc.Row(
            html.Div(f"{custs}", style={
                'font-size': '80px',
                'font-weight': 'bold',
                'color': fontCol,
            }), className='d-flex justify-content-center mt-5',),], style={
                       'padding-left':'15px',
                       'padding-right':'15px',
                       'height':  '300px',
                       'color': '#008080',
                        'background-color': bgCol,
                       'border-radius': '5px',
                       'font-size': '20px', }
    ), dcc.Graph(figure=charts.getChart(xVals=labels,
    yVals=values,
    cType='pie',
    hole=hole,
    colors=colors,
    cTitle=f'<b>Total Customers Quarterly ( {selectedYear[-1]} )</b>',
    titleColor=titleColor,
    titleFontSize=20,
    showLegend=False,
    textPosition='inside',
    textSize=18)), getRegularCustomersPerYear(year)

def getTodayCustomers():
    df = data
    df = df[df['Year'] == max(df['Year'])]
    df = df[df['Month'] == max(df['Month'])]
    df = df[df['Day'] == max(df['Day'])]
    custs = len(df['CustomerNo'].unique())
    print(custs)
    return html.Div(f"{custs}", style={
        ' font-size': '36px !important',
        ' font-weight': 'bold !important',
                        ' text-align': 'center',
    })

dropDownStyle = {
    'margin-top': '25px',
    'margin-right': '25px',
    'justify-content': 'end',
    # 'align-content': 'center',    'text-align':'center',
    'border': '1px solid #008080',
    # 'color': '#89B850',
    #   'appearance': 'none',
    'min-width': '200px',
    'box-shadow': 'none',
    'font-size': '13px',
    'margin-left': '50px',
}

def getTopCustomersBarGraph(labels, values, name):
    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker_color=fontCol,
                name=name,
            )
        ],
        layout=go.Layout(
            xaxis=dict(
                title='<b>Customer No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>{name}</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        )
    )
    fig.update_layout(
        title_text=f'<b>Top Customers ( {selectedYear[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=24,
        bargap=0.15,
        height=550,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=fig)

def getTimeLineValueBox(title, value):
    if(type(value)==int or type(value)==float):
        valint=int(value)
        val=str(value)
        if valint>10000 and valint<100000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
        elif valint>100000 and valint<1000000:
            val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
        elif valint>=1000000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
        elif valint>=1000000 and valint<10000000:
            val=val[0:1]+'.'+val[1:3]+'B'
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
                'color':fontCol,
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
            'border': '1px solid #ebebeb',
        }
    )

def getChecksTopCustomers(check, top,cType):
    df = data

    if check==0:
        name= 'Sales/10'
        df= pd.DataFrame(df.groupby('CustomerNo').TotalPrice.sum()).sort_values(
            by='TotalPrice', ascending=False)
        df['TotalPrice'] = df['TotalPrice']
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Customer {i}")
        old_values = list(df['TotalPrice'])
        values = []
        for i in old_values:
            values.append(int(i))
    
    if check == 1:

        name = 'Profit'
        df = pd.DataFrame(df.groupby('CustomerNo').TotalProfit.sum()).sort_values(
            by='TotalProfit', ascending=False)
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Customer {i}")
        old_values = list(df['TotalProfit'])
        values = []
        for i in old_values:
            values.append(int(i))

    if check == 2:

        # Items
        name = 'Items'
        df = pd.DataFrame(df.groupby('CustomerNo').ItemNo.nunique()
                          ).sort_values(by='ItemNo', ascending=False)
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Customer {i}")
        old_values = list(df['ItemNo'])
        values = []
        for i in old_values:
            values.append(int(i))

    topCust=labels[0].split(' ')[1]
    df=data[data['CustomerNo']==int(topCust)]
    # print(f"CUIST {topCust}")
    profit=round(sum(df['TotalProfit']),2)
    # print(f"PROFIT {profit}")
    sales=round(sum(df['TotalPrice']),2)
    # print(f"SALES {sales}")
    chart=charts.getChart(
        cType=cType,
        xVals=labels,
        yVals=values,
        cName=name,
        color=fontCol,
        colors=colors,
        xTitle="<b>Customer No</b>",
        yTitle=f"<b>{name}</b>",
        cTitle=f'<b>Top Customers ( {selectedYear[-1]} )</b>',
        titleColor=titleColor,
        titleFontSize=24,
        )
    # getTopCustomersBarGraph(labels, values, name)
    return dcc.Graph(figure=chart),[
       
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Top Customer', topCust),width=12)
                ),
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Sales', sales),width=12)
                
                ),
            dbc.Row(dbc.Col( getTimeLineValueBox('Profit', profit),width=12)
               ),
        
    ]

def getCustomerBubbleChart():
    fig = go.Figure()
    names = ['Hardware', 'Electrical', 'Construction', 'IT']
    sizeV = [40, 60, 80, 100]
    xV = [1, 2, 3, 4]
    yV = [10, 11, 12, 13]
    i = 0
    for name in names:
        # print(f"SIZEV {sizeV[i]}")
        fig.add_trace(go.Scatter(
            x=[xV[i]], y=[yV[i]],
            name=name,
            marker=dict(size=sizeV,
                color=[colors[i]]),
            # marker_colors=[]
        ))
        i += 1
    fig.update_layout(
        title_text=f'<b>Customers Count with Category</b>',
        height=500,
        title_font_color=titleColor,
        title_font_size=24,
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            title='<b>Customers Count</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor,
            )
        ),
        yaxis=dict(
            title=f'<b>Sales</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor,
            )
        )
    )

    return [
        dcc.Graph(figure=fig)
    ]

def getCustCreditDebit(year):
    df = data
    df = df[df['Year'] == year]
    
    cash=df[df['CustomerNo']==1]
    cash = round(sum(cash['TotalPrice']), 2)
    
    debs=df[df['CustomerNo']!=1]
    debs = round(sum(debs['TotalPrice']), 2)
    
    labels = ["Cash", "Credit"]
    
    values = [cash, debs]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                # hole=.6,
                pull=[0, 0.1],
                marker_colors=colors,
            )],

    )
    fig.update_layout(
        height=500,
        title=f'<b>Total Cash and Credit of Customers ( {selectedYear[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,
    
    )
    fig.update_traces(textposition='inside', textfont_size=18)
    return [dcc.Graph(figure=fig)]

def getNewCustomers():
    df = data
    df = df[df['Year'] == max(df['Year'])]
    df=df[df['Month']==max(df['Month'])]
    new_customers=[]
    thisMonthCustomers=list(df['CustomerNo'].unique())
    oldCustData=data[data['Year']<max(data['Year'])]
    old_customers=list(oldCustData['CustomerNo'].unique())
    for cust in thisMonthCustomers:
        if cust not in old_customers:
            new_customers.append(cust) 
    return len(new_customers)

def getRegularCustomersPerYear(year):
    df = data
    df = df[df['Year'] == year]
    months = [g for n, g in df.groupby(
        pd.Grouper(key='InvoiceDate', freq='M'))]
    custs = list(df['CustomerNo'].unique())
    for month in months:
        for cust in custs:
            if cust not in list(month['CustomerNo']):
                custs.remove(cust)
    # print(f"REGULAR CUSTOMERS {len(custs)}")
    return html.Div([
        dbc.Row([
            html.Div(f"Regular Customers ( {selectedYear[-1]} )", style={
                'font-size': '28px',
                'font-weight': 'bold',
                'margin': '10px',
                'color': titleColor,
            })
        ]),
        dbc.Row([html.Div(f"{len(custs)}", style={
            'font-size': '80px',
            'font-weight': 'bold',
             'color': fontCol,
        })], className='d-flex justify-content-center mt-5',),

    ], style={
                       'padding-left':'15px',
                       'padding-right':'15px',
                       'height':  '300px',
                       'color': '#008080',
                        'background-color': bgCol,
                       'border-radius': '5px',
                       'font-size': '20px', })

def getCustGeneralLayout():
    print(' INSIDE CUSTOMERS GENERAL TAB LAYOUT')
    return [
        # FIRST ROW
        dbc.Row(
            [
                html.Div('Select Year', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':'#20B2AA',
                     'color': titleColor,
                }),
                dcc.Dropdown(
                    id='totalCustDropDown', searchable=False, options=getYears(), value=2020, style={
                        'margin': '10px',
                        'width': '250px',
                         'color':'#008080',
                    }
                )
            ], className='d-flex justify-content-center'),
        dbc.Row(
           [
               html.Div(id='totalCustDropDownValue', className='mt-3 col-sm-6 col-md-6 col-lg-4 col-xl'
               ),
               html.Div(
                   id="regularCustomerValue", className='mt-3 col-sm-6 col-md-6 col-lg-4 col-xl'
               ),
               html.Div(html.Div(
                   html.Div([
                       dbc.Row([html.Div(f'New Customers', style={
                           'font-size': '28px',
                           'font-weight': 'bold',
                           'margin': '10px',
                          'color': titleColor,
                       })]),

                       dbc.Row([html.Div(getNewCustomers(), 
                       style={'font-size': '80px',
                      'color': fontCol,
                            'font-weight': 'bold', })], className='d-flex justify-content-center mt-5',),


                   ], style={
                       'padding-left':'15px',
                       'padding-right':'15px',
                       'height':  '300px',
                       'color': '#008080',
                        'background-color': bgCol,
                       'border-radius': '5px',
                       'font-size': '20px', })
               ), className='mt-3 col-sm-6 col-md-6 col-lg-4 col-xl'),
               html.Div(html.Div(
                   html.Div([
                       dbc.Row([html.Div(f'Today Customer Activity', style={
                           'font-size': '28px',
                           'font-weight': 'bold',
                           'margin': '10px',
                          'color': titleColor,
                       })]),

                       dbc.Row([html.Div(getTodayCustomers(), style={'font-size': '80px',   'color': fontCol,
                                                                     'font-weight': 'bold', })], className='d-flex justify-content-center mt-5',),

                       dbc.Row([html.Div(f'Shop Time 9 AM - 5 PM', style={
                           'font-size': '20px',
                           'font-weight': 'normal',
                            'color': titleColor,
                           'margin': '10px',
                       })], className='d-flex justify-content-end'),
                   ], style={
                       'padding-left':'15px',
                       'padding-right':'15px',
                       'height':  '300px',
                       'color': '#008080',
                        'background-color': bgCol,
                       'border-radius': '5px',
                       'font-size': '20px', })
                    ), className='mt-3 col-sm-6 col-md-6 col-lg-4 col-xl'),

           ]
        ),

        # SECOND ROW
        dbc.Row([
            
            html.Div(
                [
                    
                    html.Div([
                        html.I(id='total-cust-quart-chart-button', 
                                            n_clicks=0, 
                                            className='fas fa-exchange-alt fa-2x',
                                            style={'color':'black',
                                            'margin-left': '15px',
                                            'margin-top': '25px'}),
                        html.Div(id='custQuraterlyCount'),
                        ],
                        style={'background-color': 'white','height':'500px'})
                        
                        ], 
                        className='mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-4'),
            
            html.Div(html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.I(id='top-cust-chart-button', 
                                            n_clicks=0, 
                                            className='fas fa-exchange-alt fa-2x',
                                            style={'color':'black',}),
                                            
                                        ],style={'margin-left': '15px',
                                                'margin-top': '25px',
                                                }
                                    ),
                                    dbc.Col([
                                        # html.Div('Top Customers'),
                                        dcc.RadioItems(
                                            id='custRadioButtons',
                                            options=[
                                                {'label': 'Sales', 'value': 0},
                                                {'label': 'Profit', 'value': 1},
                                                {'label': 'Items', 'value': 2},
                                            ],
                                            value=0,
                                            labelStyle={
                                                'display': 'inline-block',
                                                'margin-left': '15px',
                                                'margin-top': '25px',
                                                'font-size': '18px',
                                                'font-weight': 'bold',
                                                'color': titleColor,
                                            }
                                        ),
                                        html.Div(dcc.Dropdown(id='topCustomersDropdown', searchable=False, options=[
                                            {'label': 'Top 10 Customers',
                                                'value': 10},
                                            {'label': 'Top 15 Customers',
                                                'value': 15},
                                            {'label': 'Top 20 Customers',
                                                'value': 20},
                                        ], value=15), style=dropDownStyle)

                                    ],  className='d-flex justify-content-end')

                                ]
                            ),

                            dbc.Row(
                                dbc.Col(
                                    id='custRadioValue'
                                    # dcc.Graph(),width=12
                                )
                            )

                        ],width=9,
                    ),
                    dbc.Col(id='custRadioValueBoxes',width=3),
                    ]
                ),style={'background-color': 'white','height':'500px'}), className='mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-8'),
        ], className='mt-2'),

        # THIRD ROW
        dbc.Row([

            html.Div(id='getCustCreditDebit', className='mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-4'),

            html.Div(html.Div([
                dbc.Row(
                    
                    [
                        html.Div(getCustomerBubbleChart(), className='mt-2 col-sm-8 col-md-8 col-lg-8 col-xl-9'),
                        html.Div([
       
                                dbc.Row(dbc.Col(getTimeLineValueBox('Top Category Count', 897),width=12)),

                                dbc.Row(dbc.Col(getTimeLineValueBox('Sales', 6798553),width=12)),

                                dbc.Row(dbc.Col( getTimeLineValueBox('Lowest Category', 'Hardware'),width=12)),
        
                                ], className='mt-3 col-sm-4 col-md-4 col-lg-4 col-xl-3')
            
            ] ),
            ], style={'background-color': 'white'}), className='mt-2 col-sm-12 col-md-12 col-lg-12 col-xl-8'),
        
        ], className='mt-3'),
    ]





# RADIO CALLBACK
@app.callback(
    Output("custRadioValue", "children"),
    Output("custRadioValueBoxes", "children"),
    [Input("custRadioButtons", "value"), Input(
        "topCustomersDropdown", "value"),Input("top-cust-chart-button", "n_clicks"), ],
)
def checkTopCallback(value, value2,value3):
    if int(value3)%2==0:
        topCustChartType='bar'
    else:
        topCustChartType='pie'
    print('INSIDE CHECK')
    if value == None:
        value = 0

    return getChecksTopCustomers(value, value2,topCustChartType)


# MAIN CALLBACK
@app.callback(
    Output("totalCustDropDownValue", "children"),
    Output("custQuraterlyCount", "children"),
    Output("regularCustomerValue", "children"),
    Output("getCustCreditDebit", "children"),
    [Input("totalCustDropDown", "value"),Input("total-cust-quart-chart-button", "n_clicks")],
)
def render_tab_content(value,value2):
    hole=0.4
    if value2%2==0:
        hole=0.4
    else:
        hole=0
    if value == None:
        value = 2020
    selectedYear.append(value)
    total, quarter, regular = totalCustomersPerYear(value,hole)

    return total, quarter, regular, getCustCreditDebit(selectedYear[-1])
