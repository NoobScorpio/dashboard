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
from . import itemsPage as cP
from datetime import timedelta

itemMov= pd.read_csv(
    r'./data/ItemMovement.csv')
   
itemMov= itemMov[itemMov['ItemNo']!= '.']   
itemMov['ItemNo'] = itemMov['ItemNo'].astype(int)
itemMov['MovementDate'] = pd.to_datetime(itemMov['MovementDate'])
itemMov.sort_values(by='MovementDate',inplace=True)
itemMov=itemMov[itemMov['MovementDate']!='2201-02-25']
itemMov['Year']=itemMov['MovementDate'].dt.year
itemMov['Month']=itemMov['MovementDate'].dt.month
itemMov['ItemQnty']=itemMov['InQnty']-itemMov['OutQnty']

data=cP.getData()
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors




def getItems():
    items = list(data['ItemNo'].unique())
    menuItems = []
    for cust in items:
        menuItems.append({'label': cust, 'value': cust})
    return menuItems
selectedItem=[2211]
selectedCustomers=[1]

def getCustomers(itemNo):
    df=data[data['ItemNo']==itemNo]
    custList=list(df['CustomerNo'].unique())
    menuItems = []  
    for cust in custList:
        menuItems.append({'label': cust, 'value': cust})
    return menuItems

def getItemDetailsGraph(df):       
    months = [g for n, g in df.groupby(pd.Grouper(key='InvoiceDate', freq='M'))]
    lastDate = df.tail(1)['InvoiceDate'].item()
    lastDate = pd.to_datetime(lastDate, format='%y-%m-%d')
    timeDiff = lastDate-timedelta(180)   
    timeDiff = pd.to_datetime(timeDiff, format='%y-%m-%d')
    # print(f" TIME DIFF : {timeDiff}")
    df = df[df['InvoiceDate'] > timeDiff]
    # print(df)
    dff=itemMov[itemMov['ItemQnty']<=0]
    # print(dff)
    line=pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
    figBar=go.Figure(data=[go.Line(
                marker_color=fontCol,
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=line.index,
                y=line['TotalPrice'],
                fill='tozeroy',
                fillcolor=bgCol,
                # line={
                #     'shape': 'spline',
                #     'smoothing': 1.3
                # },
            ),],layout=go.Layout(
            xaxis=dict(
                title='<b>Item No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Cost</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))
    figBar.update_layout(
        title_text=f'<b>Item {selectedItem[-1]} Timeline</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=figBar)

def getCustomerItemTimeline():
    df=data[data['ItemNo']==selectedItem[-1]]
    df=df[df['CustomerNo']==selectedCustomers[-1]]
    df=pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
    figBar=go.Figure(data=[go.Line(
                marker_color=fontCol,
                # "rgba(137, 184, 80, 1)",
                name='Sales',
                x=df.index,
                y=df['TotalPrice'],
                fill='tozeroy',
                fillcolor=bgCol,
                # line={
                #     'shape': 'spline',
                #     'smoothing': 1.3
                # },
            ),],layout=go.Layout(
            xaxis=dict(
                title='<b>Item No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Cost</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))
    figBar.update_layout(
        title_text=f'<b>Item {selectedItem[-1]} Timeline</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=figBar)

def getItemDetailsRowTwo(df):
    months = [g for n, g in df.groupby(pd.Grouper(key='MovementDate', freq='M'))]
    # print(f"LEN OF MONTHS {months}")/
    count=[]
    for i in months:
        # print(i)
        length=len(pd.DataFrame(i.groupby('MovementDate').OutQnty.count()).sort_values(by='MovementDate',ascending=False).index)
        if length!=0:
            count.append(round((30/length),2))
    
    if len(count)!=0:
        count=round(30/len(count),2)
    else:
        count=0
    # print(f"count {count}")
    # period
    dfIn=pd.DataFrame(df.groupby('MovementDate').InQnty.sum()).sort_values(by='MovementDate',ascending=False)
    dfOut=pd.DataFrame(df.groupby('MovementDate').OutQnty.sum()).sort_values(by='MovementDate',ascending=False)
    
    if count<=1: 
        if int(count)==0:
            count="1 Day"
        elif count>1 and count<4:
            count=f"3 days"
    elif count>=4 and count<=7:
        count="Less than a week"
    elif count>=4 and count<=7:
        count="More than a week"
    elif count<=12:
        count="Less than two weeks"
    elif count>=14:
        count="Half a month"
    elif count >=25:
         count="A month"
    dfIn['OutQnty']=dfOut['OutQnty']
    total=sum(dfIn['InQnty'])-sum(dfIn['OutQnty'])
    # print(dfIn)
    # print(df)
    return [ dbc.Col([
                    dbc.Row(html.Div('Available Quantity', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                'color': titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{total}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                           
                        ],className='d-flex justify-content-center'),
                    
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
            dbc.Col([
                    dbc.Row(html.Div('Selling out period', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                'color': titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{count}", style={
                                'font-size': '40px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                           
                        ],className='d-flex justify-content-center'),
                    
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
            ]

def getItemDetailsRowOne(df):
    # print(df)
    profit=round(sum(df['TotalProfit']),2)
    val=str(profit)
    if (profit>10000 and profit<100000) or (profit<-10000 and profit<-100000):
        profit=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif (profit>100000 and profit<1000000) or (profit<-100000 and profit<-1000000):
        profit=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif profit>=1000000 or profit<=-1000000:
        profit=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    
    qnty=round(sum(df['Qnty']),2)
    val=str(qnty)
    if qnty>10000 and qnty<100000:
        qnty=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif qnty>100000 and qnty<1000000:
        qnty=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif qnty>=1000000:
        qnty=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    return [

                dbc.Col([
                    dbc.Row(html.Div('Total Profit Generated', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                 'color': titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{profit}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                           
                        ],className='d-flex justify-content-center'),
                    
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
                dbc.Col([
                    
                    dbc.Row(html.Div(f'Total Quantity Sold', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                'color': titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{qnty}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                            
                        ],className='d-flex justify-content-center'),
                    
                
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color':bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),


            ]

def getSectionLayout(title="Customer Churn",thisMonth="1.42%",diff="+0.46",total="16.86%",fig=go.Figure()):
    return html.Div(html.Div([
        dbc.Row([html.Div(f'{title}', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color':"#008080",
        })], className='d-flex justify-content-center mt-1',),
        dbc.Row(
            [

                dbc.Col([
                    dbc.Row(html.Div('Last Month', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{thisMonth}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                            }),
                            html.Div(f"({diff})", style={
                                'font-size': '28px',
                                'font-weight': 'normal',
                                'margin-top': '25px',
                            }),
                        ],className='d-flex justify-content-center'),
                    dbc.Row('vs. Previous Month',className='d-flex justify-content-center'),
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': 'rgba(199,235,233,0.2)',
                    'border-radius': '5px',
                    'font-size': '20px', }),
                dbc.Col([
                    
                    dbc.Row(html.Div('Total', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{total}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                            }),
                            
                        ],className='d-flex justify-content-center'),
                    dbc.Row('Last 12 Months',className='d-flex justify-content-center'),
                
                ], style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': 'rgba(199,235,233,0.2)',
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
        'font-size': '20px', }),className='mt-2 col-sm-12 col-xl')

def itemDetails():

    return html.Div(html.Div([
        dbc.Row(
            [
            dbc.Col(html.Div(f'Item Details', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color':titleColor,
            }),className='d-flex justify-content-center mt-1',),
            
            
            ], className='d-flex justify-content-center mt-1',),
        
        
        dbc.Row(
            id='itemDetailsRowOne', className='d-flex justify-content-center mt-1',),
        dbc.Row(
            id='itemDetailsRowTwo', className='d-flex justify-content-center mt-1',),

        dbc.Row(
            [
                dbc.Col(id='itemDetailsGraph', style={
                    'margin-bottom': '10px',
                    }),


            ], className='d-flex justify-content-center mt-1',),


    ], style={
        'margin-top': '10px',
        'color': 'white',
        'margin': '10px',
        'background-color': 'white',
        'border-radius': '5px',
        'font-size': '20px', }),className='mt-2 col-sm-12 col-xl')

@app.callback(
    Output('itemDetailsRowOne','children'),
    Output('itemDetailsRowTwo','children'),
     Output('itemDetailsGraph','children'),
    [Input('itemDetaailsDropDown','value')]
)
def itemDetailsDropDown(value):
    if value==None:
        value=2211
    selectedItem.append(value)
    df=data[data['ItemNo']==value]
    df1=itemMov[itemMov['ItemNo']==value]
    # getItemDetailsRowTwo(df1)
    return getItemDetailsRowOne(df),getItemDetailsRowTwo(df1),getItemDetailsGraph(df)

def getItemCustomerTimeline():  
    return html.Div(html.Div([
        dbc.Row(
            [
            dbc.Col(html.Div(f'Items\'s Customers Timeline', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color':"#008080",
            'color': titleColor,
            }),className='d-flex justify-content-center mt-1',),

            ], className='d-flex justify-content-center mt-1',),
        
        dbc.Row([
          
            dbc.Col(
                dbc.Row(
                    [

                html.Div('Select Customer',style={
                     'margin': '10px',
                                    'margin-top': '15px',
                                   'font-size': '26px',
                                    'font-weight': 'bold',
                                     'color':titleColor,
                }),
                
                html.Div(  
                    dcc.Dropdown(id='cust_itemCustAdvancedDropdown', 
                    searchable=False, 
                    options=getCustomers(selectedItem[-1]), 
                    value=1, 
                    style={'margin': '10px',
                         'width': '250px',
                          'color':titleColor,
                                    }
                                ),style={
                    'margin': '10px',
                    'color':"#008080",
                }
                )

                ]
                ),className='d-flex justify-content-center mt-1',)]),
            
            dbc.Row(
                dbc.Col(
                    id="custItemAdvancedTimeline"
                ),
            ),
    


    ], style={
        'margin-top': '10px',
        'color': 'white',
        'margin': '10px',
        'background-color': 'white',
        'border-radius': '5px',
        'font-size': '20px', }),className='mt-2 col-sm-12 col-xl')


@app.callback(
    Output('custItemAdvancedTimeline','children'),
    [Input('cust_itemCustAdvancedDropdown','value')]
)
def itemCustDetailsDropDown(value):
    if value==None: 
        value=1
    selectedCustomers.append(value)
    
    return getCustomerItemTimeline()

def getHighDemandItems():
    df=pd.DataFrame(data.groupby('ItemNo').Qnty.sum()).sort_values(by='Qnty',ascending=False).head(10)
    indexes=[]
    for i in df.index:
        indexes.append(f"Item {i}")
    figBar=go.Figure(data=[go.Bar(
        x=indexes, 
        y=df['Qnty'],
        marker_color=fontCol,
        )],layout=go.Layout(
            xaxis=dict(
                title='<b>Item No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Cost</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    figBar.update_layout(
        title_text=f'<b>Top 10 High Demand Items</b>',
        title_font_size=20,
        showlegend=False,
        # height=500,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return html.Div(html.Div(dcc.Graph(figure=figBar)),className='mt-2 col-sm-12 col-xl')

def get15ExpensiveItems():
    df=data
    top=pd.DataFrame(df.groupby('ItemNo').Cost.mean()).sort_values(by='Cost',ascending=False)
    total=sum(top['Cost'])
    
    top=top.head(15)

    topItemsPercentage=round((sum(top['Cost'])/total)*100,2)
    otherItemsPercentage=100-topItemsPercentage
    indexes=[]
    for i in top.index:
        indexes.append(f"Item {i}")
    # print(top)

    topSales=0
    otherSales=0
    otherSalesDf=df
    j=0
    for i in top.index:
        otherSalesDf=otherSalesDf[otherSalesDf['ItemNo']!=int(i)]
        # print(otherSalesDf)

    totalSales=round(sum(df['TotalPrice']),2)
    otherSales=round(sum(otherSalesDf['TotalPrice']),2)
    topSales=totalSales-otherSales
    
    val=str(topSales)
    if (topSales>10000 and topSales<100000):
        topSales=val[0:1]+val[1:2]+'.'+val[2:3]+'K'   
    elif (topSales>100000 and topSales<1000000) :
        topSales=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif topSales>=1000000 :
        topSales=val[0:1]+val[1:2]+'.'+val[2:3]+'M'


    
    val=str(otherSales)
    if (otherSales>10000 and otherSales<100000):
        otherSales=val[0:1]+val[1:2]+'.'+val[2:3]+'K'   
    elif (otherSales>100000 and otherSales<1000000) :
        otherSales=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif otherSales>=1000000 :
        otherSales=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    
    
    labels = ['Oxygen','Hydrogen','Carbon_Dioxide','Nitrogen']
    values = [4500, 2500, 1053, 500]

    figBar=go.Figure(data=[go.Bar(
        x=indexes, 
        y=top['Cost'],
        marker_color=fontCol,
        )],layout=go.Layout(
            xaxis=dict(
                title='<b>Item No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Cost</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))
    figBar.update_layout(
        title_text=f'<b>Top 15 Items Cost</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    fig = go.Figure(
        data=[
            go.Pie(
                labels=
                ['Top Expensive Items', 'Other Items'], 
                values=
                [topItemsPercentage,otherItemsPercentage],
                marker_colors=colors,
                pull=[0.1,0])
                ],
                
                )
    fig.update_layout(
         margin=dict(l=0, r=0, t=10, b=0),
        height=400,
        # title=f'<b>Top 15 vs Others</b>',
        # title_font_color=titleColor,
        # title_font_size=20,
        showlegend=False,

    )
    fig.update_traces(textposition='inside', textfont_size=18)
    return html.Div(html.Div([
        dbc.Row([html.Div(f'Top 15 Expensive Items', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color':titleColor,
        })], className='d-flex justify-content-center mt-1',),
        dbc.Row(
            [

                dbc.Col([
                    # FIRST ROW
                    dbc.Row(dbc.Col([
                        dbc.Row(html.Div('Top Expensive Items Percentage', style={
                                'font-size': '24px',
                                'font-weight': 'nornaml',
                                'color': titleColor,
                                'margin-top': '10px',
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{topItemsPercentage}%", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                 'color': fontCol,
                            }),
                            html.Div(f"({otherItemsPercentage}%)", style={
                                'font-size': '28px',
                                'font-weight': 'normal',
                                'margin-top': '25px',
                                'color': fontCol,
                            }),
                        ],className='d-flex justify-content-center'),
                    dbc.Row(
                        'vs. Other Items',className='d-flex justify-content-center'
                        ,style={ 'color': titleColor,}
                        
                        ),
                    ]), style={
                    'height':  '200px',
                    
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
                    # SECOND ROW
                    dbc.Row(dbc.Col([
                        dbc.Row(html.Div('Sales', style={
                                'font-size': '28px',
                                'font-weight': 'nornaml',
                                'margin-top': '10px',
                                'color': titleColor,
                            }),className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{topSales}", style={
                                'font-size': '42px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                            html.Div(f"({otherSales})", style={
                                'font-size': '28px',
                                'font-weight': 'normal',
                                'margin-top': '20px',
                                   'color': fontCol,
                            }),
                        ],className='d-flex justify-content-center'),
                    dbc.Row('vs. Other Items',className='d-flex justify-content-center',style={ 'color': '#008080',}),
                    ]), style={
                    'height':  '200px',
                    'color': '#008080',
                    'margin': '10px',
                    'background-color': bgCol,
                    'border-radius': '5px',
                    'font-size': '20px', }),
                ],width=6),
                
                dbc.Col(dcc.Graph(figure=fig), style={
                    'height':  '200px',
                    'color': '#008080',
                    # 'margin': '10px',
                    # 'background-color': 'rgba(199,235,233,0.2)',
                    'border-radius': '5px',
                    'font-size': '20px', },width=6),


            ], className='d-flex justify-content-center mt-1',),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=figBar), style={
                    'margin-bottom': '10px',
                    }),


            ], className='d-flex justify-content-center mt-1',),


    ], style={
        'margin-top': '10px',
        'color': 'white',
        'margin': '10px',
        'background-color': 'white',
        'border-radius': '5px',
        'font-size': '20px', }),className='mt-2 col-sm-12 col-xl')

def itemInOutQuantityTimeLine():
    df=itemMov
    df=df[df['Year']==max(df['Year'])]
    df=df[df['Month']==max(df['Month'])]
    # print(df)
    dfIn=pd.DataFrame(df.groupby('MovementDate').InQnty.sum())
    dfOut=pd.DataFrame(df.groupby('MovementDate').OutQnty.sum())
    figBar=go.Figure(
        data=[
            go.Line(
                marker_color=fontColDark,
                # "rgba(137, 184, 80, 1)",
                name='In Quantity',
                x=dfIn.index,
                y=dfIn['InQnty'],
                fill='tozeroy',
                fillcolor=bgCol,
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
            ),
            go.Line(
                marker_color=fontCol,
                # "rgba(137, 184, 80, 1)",
                name='Out Quantity',
                x=dfOut.index,
                y=dfOut['OutQnty'],
                fill='tozeroy',
                fillcolor=bgCol,
                line={
                    'shape': 'spline',
                    'smoothing': 1.3
                },
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
        ))
    figBar.update_layout(
        title_text=f'<b>Item {selectedItem[-1]} Last Month Timeline</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return html.Div(html.Div(dcc.Graph(figure=figBar), style={
                    'margin-top': '10px',
                    'color': 'white',
                    'margin': '10px',
                    'background-color': 'white',
                    'border-radius': '5px',
                    'font-size': '20px', }),className='mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-6')
      
            
           

def getYearInOutQuantity():
    df=itemMov
    dfIn=pd.DataFrame(df.groupby('Year').InQnty.sum())
    dfOut=pd.DataFrame(df.groupby('Year').OutQnty.sum())
    figBar=go.Figure(
        data=[
            go.Bar(
                marker_color=fontColDark,
                name='In Quantity',
                x=dfIn.index,
                y=dfIn['InQnty'],
            ),
            go.Bar(
                marker_color=fontCol,
                name='Out Quantity',
                x=dfOut.index,
                y=dfOut['OutQnty'],

            ),
            ],
            layout=go.Layout(
            xaxis=dict(
                title='<b>Years</b>',
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
    figBar.update_layout(
        title_text=f'<b>Items In and Out Quantity Yearly</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return html.Div(html.Div(dcc.Graph(figure=figBar), style={
        'margin-top': '10px',
        'color': 'white',
        'margin': '10px',
        'background-color': 'white',
        'border-radius': '5px',
        'font-size': '20px', }),className='mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-6')

def getAdvancedLayout():
    return [
        # MAIN ROW
        dbc.Row(
            # MAIN COL
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div("Select Item", style={
                                    'margin': '10px',
                                    'margin-top': '15px',
                                   'font-size': '26px',
                                    'font-weight': 'bold',
                                     'color':titleColor,
                                }),className='d-flex justify-content-end mt-1',),
                    dbc.Col(html.Div( dcc.Dropdown(
                                id='itemDetaailsDropDown', searchable=False, options=getItems(), value=selectedItem[-1], style={
                                    'margin': '10px',
                                    'width': '250px',
                                     'color':titleColor,
                                }
                            )
                            ,style={
                #     'font-size': '32px',
                #     'font-weight': 'bold',
                'margin': '10px',
                'color':"#008080",
            }
            ),className='d-flex justify-content-start mt-1',)
                ],className='d-flex justify-content-center mt-1',),
        dbc.Row(

                  [
                      get15ExpensiveItems(),
                      itemDetails(),
                  ]
                ),
        
        dbc.Row(
                  [
                      getYearInOutQuantity(),
                      itemInOutQuantityTimeLine(),
                      
                  ]
                ),
       
        dbc.Row(
                  [
                     getItemCustomerTimeline(),
                     
                    getHighDemandItems(),
                  ]
                ),
            ],width=12),

        ),
    ]