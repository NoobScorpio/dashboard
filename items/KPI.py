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

data=cP.getData()
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors
itemMov= pd.read_csv(
    r'./data/ItemMovement.csv')
   
itemMov= itemMov[itemMov['ItemNo']!= '.']   
itemMov['ItemNo'] = itemMov['ItemNo'].astype(int)
itemMov['InQnty'] = itemMov['InQnty'].astype(int)
itemMov['OutQnty'] = itemMov['OutQnty'].astype(int)
itemMov['MovementDate'] = pd.to_datetime(itemMov['MovementDate'])
itemMov.sort_values(by='MovementDate',inplace=True)
itemMov=itemMov[itemMov['MovementDate']!='2201-02-25']
itemMov['Year']=itemMov['MovementDate'].dt.year
itemMov['Month']=itemMov['MovementDate'].dt.month
itemMov['ItemQnty']=itemMov['InQnty']-itemMov['OutQnty']
monthNames = [1,2,3,4,5,6,7,8,9,10,11,12]
mNames = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

def avgItemPerDay():
    df=pd.DataFrame(data.groupby('InvoiceDate').Qnty.sum())
    avg=round(df['Qnty'].mean(),2)
    val=str(avg)
    if (avg>10000 and avg<100000):
        avg=val[0:1]+val[1:2]+'.'+val[2:3]+'K'   
    elif (avg>100000 and avg<1000000) :
        avg=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif avg>=1000000 :
        avg=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    return [
        dbc.Row(
            [
                dbc.Col(html.Div('Average Quantity per day', style={
                        'font-size': '28px',
                        'font-weight': 'bold',
                        'margin': '10px',
                        'color':titleColor,
                        })),


            ]
        ),
        dbc.Row(
            html.Div(f"{avg}", style={
                'font-size': '80px',
                'font-weight': 'bold',

            }), className='d-flex justify-content-center mt-5',),

    ]

def avgItemPerTrans():
    df=pd.DataFrame(data.groupby('InvoiceNo').Qnty.sum())
    avg=round(df['Qnty'].mean(),2)
    return [
        dbc.Row(
            [
                dbc.Col(html.Div('Average Quantity per Transaction', style={
                        'font-size': '28px',
                        'font-weight': 'bold',
                        'margin': '10px',
                        'color':titleColor,
                        })),


            ]
        ),
        dbc.Row(
            html.Div(f"{avg}", style={
                'font-size': '80px',
                'font-weight': 'bold',

            }), className='d-flex justify-content-center mt-5',),

    ]

def sellThroughRate():
    dailyMostSoldItems()
    df=itemMov
    df = [g for n, g in df.groupby(pd.Grouper(key='MovementDate', freq='M'))]
    i=-1
    j=1
    values=[]
    # outValues=[]
    labels=[]
    while True:
        if df[i].empty:
            i-=1
            continue

        else:
            month=list(df[i]['Month'].unique())
            year=list(df[i]['Year'].unique())
            values.append( round(sum(df[i]['OutQnty'])/  sum(df[i]['InQnty'])* 100 ,2)  )
            labels.append(f" {mNames[month[0]-1]}, {year[0]}")
            i-=1
            
            if i<=-12 and len(values)>=12:
                break
    labels.reverse()
    values.reverse()
    total=round(sum(values),1)

    last=values[-1]
    prev=values[-2]

    diff=round(last-prev,2)
    if diff>0:
        diff=f"+{diff}"

    fig=go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=labels,
            marker_color=fontColDark,
            y=values,
            name='Churn %'
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
                title=f'<b>Sell-Through %</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>Last 12 Month Sell-Through Rate</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    # print(df)
    return getSectionLayout(title="Sell-Through Rate",thisMonth=f"{last}%",diff=diff,total=f'{total}%',fig=fig)

def stockToSalesRatio():
    dfItem=itemMov
    dfItem = [g for n, g in dfItem.groupby(pd.Grouper(key='MovementDate', freq='M'))]
    dfSales=data
    dfSales = [g for n, g in dfSales.groupby(pd.Grouper(key='InvoiceDate', freq='M'))]
    i=-1
    j=1
    values=[]
    # outValues=[]
    labels=[]
    while True:
        if dfItem[i].empty or dfSales[i].empty:
            i-=1
            continue

        else:
            print(f"{j} : {dfItem[i]['Month']}")
            month=list(dfItem[i]['Month'].unique())
            year=list(dfItem[i]['Year'].unique())
            value=round((sum(dfItem[i-1]['InQnty'])-sum(dfItem[i-1]['OutQnty']))/sum(dfSales[i]['TotalPrice']),2)
            values.append(value)
            print(f"{j}: {month[0]}")
            labels.append(f" {mNames[month[0]-1]}, {year[0]}")
            i-=1
            j+=1
            if i<=-12 and len(values)>=12:
                break
    labels.reverse()
    values.reverse()
    total=round(sum(values),1)

    last=values[-1]
    prev=values[-2]

    diff=round(last-prev,2)
    if diff>0:
        diff=f"+{diff}"

    fig=go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=labels,
            marker_color=fontColDark,
            y=values,
            name='Churn %'
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
                title=f'<b>Stock-to-Sales Ratio</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                    color=titleColor
                )
            )
        ))

    fig.update_layout(
        title_text=f'<b>Last 12 Month Stock-to-Sales Ratio</b>',
        title_font_size=20,

        title_font_color=titleColor,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    # print(df)
    return getSectionLayout(title="Stock-to-Sales Ratio",thisMonth=f"{last}%",diff=diff,total=f'{total}%',fig=fig) 

def getSectionLayout(title="Customer Churn",thisMonth="1.42%",diff="+0.46",total="16.86%",fig=go.Figure()):
    return html.Div(html.Div([
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
        'font-size': '20px', }),className='mt-2 col-sm-12 col-xl')

def dailyMostSoldItems():

    df=data
    df=pd.DataFrame(df.groupby(['InvoiceDate','ItemNo']).Qnty.sum())
    print('DOUBLE GROUPBY')
    # df['InvoiceDate'],df['ItemNo']=df.index
    datel,iteml=[],[]
    i=0
    for date,item in df.index:
        datel.append(date)
        iteml.append(item)  
        i+=1
        if i>100:   
            break
    print(datel,iteml)
    # print(df.head(25))
    # df=df.groupby(level=1).apply(max)

    # print(df)a    

def getKPILayout():
    return [
        dbc.Row(
            [
                dbc.Col(avgItemPerTrans(), style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'margin-top': '10px',
                   'color': fontCol,
                   'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ),
               dbc.Col(avgItemPerDay(), style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'margin-top': '10px',
                   'color': fontCol,
                   'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ),
            #    dbc.Col(dailyMostSoldItems(), style={
            #        'height':  '300px',
            #        # 'display': 'flex',
            #        # 'width':   '90%',
            #        'margin-top': '10px',
            #        'color': fontCol,
            #        'margin': '10px',
            #        'background-color': bgCol,
            #        'border-radius': '5px',
            #        'font-size': '20px', }
            #    ),
        ]),
        dbc.Row([
           sellThroughRate(),
           stockToSalesRatio(),
        ]),
    ]