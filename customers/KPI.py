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
from . import customersPage as cP
import numpy as np

data = cP.getData()
data['Month'] = data['Month'].astype(int)
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
monthNames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
mNames = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

data['CustomerNo'] = data['CustomerNo'].astype(int)
titleColor = cP.titleColor
fontCol = cP.fontCol
fontColDark = cP.fontColDark
bgCol = cP.bgCol
colors = cP.Colors


def getAvgCustsPerDay():
    df = data
    avg = pd.DataFrame(df.groupby('InvoiceDate').CustomerNo.count())
    avg = int(avg['CustomerNo'].mean())
    print(avg)
    return avg


def getAvgSalesPerCust():
    df = data
    avg = pd.DataFrame(df.groupby('InvoiceDate').TotalPrice.sum())
    avg = round(avg['TotalPrice'].mean(), 2)
    print(avg)
    return html.Div(avg)


def getLoyalCustomersRate():
    df = data

    thisYearCusts = df[df['Year'] == max(df['Year'])]
    thisYearCusts = thisYearCusts[thisYearCusts['Month'] == max(
        thisYearCusts['Month'])]
    thisYearCusts = pd.DataFrame(
        thisYearCusts.groupby('CustomerNo').InvoiceDate.count())

    thisYearTotalCusts = len(thisYearCusts)
    thisYearloyality = []

    thisCustsCounts = list(thisYearCusts['InvoiceDate'])
    for no in thisCustsCounts:
        thisYearloyality.append(round(no/thisYearTotalCusts, 2))

    thisAvg = 0
    for i in thisYearloyality:
        thisAvg += i
    thisAvg = round(thisAvg/len(thisYearloyality), 2)

    prevYearCusts = df[df['Year'] == max(df['Year'])]
    prevYearCusts = prevYearCusts[prevYearCusts['Month'] == max(
        prevYearCusts['Month'])-1]
    prevYearCusts = pd.DataFrame(
        prevYearCusts.groupby('CustomerNo').InvoiceDate.count())

    prevYearTotalCusts = len(prevYearCusts)
    prevYearloyality = []

    prevCustsCounts = list(prevYearCusts['InvoiceDate'])
    for no in prevCustsCounts:
        prevYearloyality.append(round(no/prevYearTotalCusts, 2))

    prevAvg = 0
    for i in prevYearloyality:
        prevAvg += i
    le=len(prevYearloyality) if len(prevYearloyality)!=0 else 1
    prevAvg = round(prevAvg/le, 2)

    diff = round(thisAvg-prevAvg, 2)
    if diff > 0:
        diff = f"+{diff}"
    else:
        diff = f"-{diff}"
    print(thisYearCusts)
    return dbc.Col([
        dbc.Row([
            html.Div(f"{thisAvg}", style={
                'font-size': '50px',
                'font-weight': 'bold',
                'margin': '10px',
                'color': fontCol,
            }),
            html.Div(f"({diff})", style={
                'font-size': '28px',
                'font-weight': 'normal',
                'margin-top': '25px',
                'color': fontCol,
            }),
        ]),

    ], width=12, className="d-flex justify-content-center")


def getCustomerLifetimeValue():
    df = data
    df = df[df['Year'] == max(df['Year'])]

    thisMonth = df[df['Month'] == max(df['Month'])]

    thisValue = sum(thisMonth['TotalProfit'])

    prevMonth = df[df['Month'] == max(df['Month'])-1]
    prevValue = round(sum(prevMonth['TotalProfit']), 2)

    diff = thisValue-prevValue

    val = str(thisValue)
    if thisValue > 10000 and thisValue < 100000:
        thisValue = val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif thisValue > 100000 and thisValue < 1000000:
        thisValue = val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif thisValue >= 1000000:
        thisValue = val[0:1]+val[1:2]+'.'+val[2:3]+'M'

    val = str(diff)
    if (diff > 10000 and diff < 100000) or (diff < -10000 and diff > -100000):
        if diff > 0:
            diff = "+"+val[0:1]+val[1:2]+'.'+val[2:3]+'K'
        else:
            diff = val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif (diff > 100000 and diff < 1000000) or (diff < -100000 and diff > -1000000):
        if diff > 0:
            diff = "+"+val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
        else:
            diff = val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'

    elif diff >= 1000000 or diff <= -1000000:
        if diff > 0:
            diff = "+"+val[0:1]+val[1:2]+'.'+val[2:3]+'M'
        else:
            diff = val[0:1]+val[1:2]+'.'+val[2:3]+'M'

    return dbc.Col([
        dbc.Row([
            html.Div(f"{thisValue}", style={
                'font-size': '50px',
                'font-weight': 'bold',
                'margin': '10px',
                'color': fontCol,
            }),
            html.Div(f"({diff})", style={
                'font-size': '28px',
                'font-weight': 'normal',
                'margin-top': '25px',
                'color': fontCol,
            }),
        ]),

    ], width=12, className="d-flex justify-content-center")


def getKPIRushHour():
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[1, 2, 10, 4, 1, 2, 10, 4],
        theta=["3Pm", "1PM", "11Am", "9AM", "3Pm", "1PM", "11Am", "9AM"],

    ))
    fig.update_layout(
        showlegend=True
    )
    return dcc.Graph(figure=fig)


def getMonthlyCustomerChurn():
    df = data[data['Year'] == max(data['Year'])-1]
    prevdf = data[data['Year'] == max(df['Year'])-2]
    monthy_customers = []
    monthy_customers.append(list(df['Month'].unique()))

    prevM, nowM = [], []
    for i in monthNames:
        if i != 12:
            if i == 1:
                prev = prevdf[prevdf['Month'] == max(prevdf['Month'])]
                now = df[df['Month'] == i]
                prev = list(prev['CustomerNo'].unique())
                now = list(now['CustomerNo'].unique())
                prevM.append(len(prev))
                nowM.append(len(now))

            prev = df[df['Month'] == i-1]
            now = df[df['Month'] == i]
            prev = list(prev['CustomerNo'].unique())
            now = list(now['CustomerNo'].unique())
            prevM.append(len(prev))
            nowM.append(len(now))
    churn = []
    for i, j in zip(prevM, nowM):
        if i == 0:
            churn.append((i-j)/1)
        else:
            churn.append((i-j)/i)
    print(f"CHURN {churn}")
    churn[1] = churn[1]/100
    fig = go.Figure(data=[
        go.Bar(
            x=mNames,
            y=churn,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=mNames,
            marker_color=fontColDark,
            y=churn,
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
            title=f'<b>Churn %</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor
            )
        )
    ))

    fig.update_layout(
        title_text=f'<b>Monthly Customer Churn Rate</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    diff = round(churn[-1]-churn[-2], 2)
    if diff > 0:
        diff = f"+{diff}"
    else:
        diff = f"{diff}"

    return fig, diff, round(churn[-1], 2)
    # churnRate = 0
    # for i in churn:
    #     churnRate += i
    # churnRate = churnRate/len(churn)


def getRevenueChurn():
    df = data[data['Year'] == max(data['Year'])-1]
    prevdf = data[data['Year'] == max(df['Year'])-2]
    prevRc, nowRc, prevCC, nowCC = [], [], [], []
    for i in monthNames:
        if i != 2020:
            if i == 1:
                prev = prevdf[prevdf['Month'] == max(prevdf['Month'])]
                rc = pd.DataFrame(prev.groupby('CustomerNo').TotalPrice.sum())
                rc = sum(rc['TotalPrice'])
                prevRc.append(rc)
                cc = len(list(prev['CustomerNo'].unique()))
                prevCC.append(cc)

                now = df[df['Month'] == max(df['Month'])]
                rc = pd.DataFrame(now.groupby('CustomerNo').TotalPrice.sum())
                rc = sum(rc['TotalPrice'])
                nowRc.append(rc)
                cc = len(list(now['CustomerNo'].unique()))
                nowCC.append(cc)

        prev = prevdf[prevdf['Month'] == i-1]
        rc = pd.DataFrame(prev.groupby('CustomerNo').TotalPrice.sum())
        rc = sum(rc['TotalPrice'])
        prevRc.append(rc)
        cc = len(list(prev['CustomerNo'].unique()))
        prevCC.append(cc)

        now = df[df['Month'] == i]
        rc = pd.DataFrame(now.groupby('CustomerNo').TotalPrice.sum())
        rc = sum(rc['TotalPrice'])
        nowRc.append(rc)
        cc = len(list(now['CustomerNo'].unique()))
        nowCC.append(cc)

    churn = []

    for i, j in zip(nowCC, prevCC):
        if i == 0:
            churn.append(round(((i-j)/1)*100, 2))
        else:
            churn.append(round(((i-j)/i)*100, 2))

    j = 0
    for i in prevRc:
        if i == 0:
            print(f"YES ZERO")
            # print(f"PREV RC  VALUE {i} PREVIOUS ")

            prevRc[j] = prevRc[j-1]
        j += 1

    j = 0
    for i in nowRc:
        if i == 0:
            print(f"YES ZERO")
            # print(f"PREV RC  VALUE {i} PREVIOUS ")

            nowRc[j] = nowRc[j-1]
        j += 1

    # print(f"PREV RC {prevRc}")

    rc = []
    k = 0
    for i, j in zip(nowRc, prevRc):
        if i == 0:
            rc.append(round(((i-j)/1)*10, 2))
        else:
            if j == 0:
                rc.append(round(((i-j)/i)*10, 2))
                print(f"REVENUE CHURN : {round( ((i-j)/1)*100 ,2)}")
            else:
                rc.append(round(((i-j)/i)*10, 2))
                print(f"REVENUE CHURN : {round( ((i-j)/i)*100 ,2)}")
        k += 1
        print(f"NOW REVENUE CHURN : {i} , Prev REVENUE CHURN : {j}")

    total = 0

    for i in rc:
        if np.isnan(i):
            total += 0
        else:
            total += i
        # print(f"MRR {i} and TOTAL {total}")
    total = round(total, 2)

    fig = go.Figure(data=[
        go.Bar(
            x=mNames,
            y=rc,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=mNames,
            marker_color=fontColDark,
            y=rc,
            name='Revenue Churn'
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
            title=f'<b>Revenue Churn</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor
            )
        )
    ))

    fig.update_layout(
        title_text=f'<b>Monthly Revenue Churn</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    diff = round(rc[-1]-rc[-2], 2)
    if diff > 0:
        diff = f"+{diff}"
    if diff == 0:
        diff = f"+{diff}"
    return getSectionLayout(title="Revenue Churn", thisMonth=f"{round(rc[-1],2)}%", diff=diff, total=f"{total}%", fig=fig)


def getMRR():
    df = data[data['Year'] == max(data['Year'])-1]
    prevdf = data[data['Year'] == max(df['Year'])-2]
    prevM, nowM = [], []
    for i in monthNames:
        if i != 12:
            if i == 1:
                prev = prevdf[prevdf['Month'] == max(prevdf['Month'])]

                avgRev = pd.DataFrame(prev.groupby(
                    'CustomerNo').TotalPrice.sum())
                avgRev = avgRev['TotalPrice'].mean()
                accounts = len(list(prev['CustomerNo'].unique()))
                mrr = round(avgRev*accounts, 2)
                prevM.append(mrr)

                now = df[df['Month'] == i]
                avgRev = pd.DataFrame(now.groupby(
                    'CustomerNo').TotalPrice.sum())
                avgRev = avgRev['TotalPrice'].mean()
                accounts = len(list(now['CustomerNo'].unique()))
                mrr = round(avgRev*accounts, 2)
                nowM.append(mrr)

            prev = df[df['Month'] == i-1]
            avgRev = pd.DataFrame(prev.groupby('CustomerNo').TotalPrice.sum())
            avgRev = avgRev['TotalPrice'].mean()
            accounts = len(list(prev['CustomerNo'].unique()))
            mrr = round(avgRev*accounts, 2)
            prevM.append(mrr)

            now = df[df['Month'] == i]
            avgRev = pd.DataFrame(now.groupby('CustomerNo').TotalPrice.sum())
            avgRev = avgRev['TotalPrice'].mean()
            accounts = len(list(now['CustomerNo'].unique()))
            mrr = round(avgRev*accounts, 2)
            nowM.append(mrr)
    monthly_mrr = []
    for j, i in zip(prevM, nowM):
        if i == 0:
            mrr = round(((j-i)/1)*100, 2)
        else:
            mrr = round(((j-i)/i)*100, 2)
        monthly_mrr.append(mrr)
        # print(mrr)

    total = 0
    for i in monthly_mrr:
        if np.isnan(i):
            total += 0
        else:
            total += i
        # print(f"MRR {i} and TOTAL {total}")
    total = round(total, 2)

    fig = go.Figure(data=[
        go.Bar(
            x=mNames,
            y=monthly_mrr,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=mNames,
            marker_color=fontColDark,
            y=monthly_mrr,
            name='MRR Growth'
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
            title=f'<b>MRR Growth</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor
            )
        )
    ))

    fig.update_layout(
        title_text=f'<b>Monthly MRR Growth</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    diff = round(monthly_mrr[-1]-monthly_mrr[-2], 2)
    if diff > 0:
        diff = f"+{diff}"
    if diff == 0:
        diff = f"+{diff}"
    return getSectionLayout(title="MRR Growth", thisMonth=f"{round(monthly_mrr[-1],2)}%", diff=diff, total=f"{total}%", fig=fig)


def getRetentionRate():
    df = data[data['Year'] == max(data['Year'])-1]
    prevdf = data[data['Year'] == max(df['Year'])-2]
    monthy_customers = []
    monthy_customers.append(list(df['Month'].unique()))
    prevM, nowM = [], []
    for i in monthNames:
        if i != 12:
            if i == 1:
                prev = prevdf[prevdf['Month'] == max(prevdf['Month'])]
                now = df[df['Month'] == i]
                prev = list(prev['CustomerNo'].unique())
                now = list(now['CustomerNo'].unique())
                prevM.append(len(prev))
                nowM.append(len(now))

            prev = df[df['Month'] == i-1]
            now = df[df['Month'] == i]
            prev = list(prev['CustomerNo'].unique())
            now = list(now['CustomerNo'].unique())
            prevM.append(len(prev))
            nowM.append(len(now))

    retention = []
    for j, i in zip(prevM, nowM):
        if i == 0:
            retention.append(round(((j-(j-i))/1)*100, 2))
        else:
            retention.append(round(((j-(j-i))/i)*100, 2))
    total = 0
    for i in retention:
        total += i
    # total=round(total/len(retention))
    fig = go.Figure(data=[
        go.Bar(
            x=mNames,
            y=retention,
            marker_color=bgCol,
            name='Month'
        ),
        go.Line(
            x=mNames,
            marker_color=fontColDark,
            y=retention,
            name='Retention Rate'
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
            title=f'<b>Retention Rate</b>',
            titlefont=dict(
                # family='Courier New, monospace',
                size=18,
                color=titleColor
            )
        )
    ))

    fig.update_layout(
        title_text=f'<b>Monthly Customer Retention Rate</b>',
        title_font_size=20,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
    )

    diff = round(retention[-1]-retention[-2], 2)
    if diff > 0:
        diff = f"+{diff}"
    if diff == 0:
        diff = f"+{diff}"
    return getSectionLayout(title="Customer Retention", thisMonth=f"{round(retention[-1],2)}%", diff=diff, total=f"{total}%", fig=fig)


def getTotalChurn():
    prevL, nowL = [], []
    for i in yearsName:
        if i != 2020:
            prev = data[data['Year'] == i]
            now = data[data['Year'] == i+1]
            prev = list(prev['CustomerNo'].unique())
            now = list(now['CustomerNo'].unique())
            prevL.append(len(prev))
            nowL.append(len(now))
        #
    churn = []
    for j, i in zip(prevL, nowL):
        if i == 0:
            churn.append((i-j)/1)

        else:
            churn.append((i-j)/i)
    churnRate = 0
    for i in churn:
        churnRate += i
    churnRate = churnRate/len(churn)

    return f"{round(churnRate,2)}%"


def getCustomerChurn():
    total = getTotalChurn()
    getMRR()
    fig, diff, thisMonth = getMonthlyCustomerChurn()
    return getSectionLayout("Customer Churn", thisMonth=thisMonth, diff=diff, total=total, fig=fig)


def getSectionLayout(title="Customer Churn", thisMonth="1.42%", diff="+0.46", total="16.86%", fig=go.Figure()):
    return html.Div(html.Div([
        dbc.Row([html.Div(f'{title}', style={
            'font-size': '32px',
            'font-weight': 'bold',
            'margin': '10px',
            'color': titleColor,

        })], className='d-flex justify-content-center mt-1',),
        dbc.Row(
            [

                dbc.Col([
                    dbc.Row(html.Div('Last Month', style={
                        'font-size': '28px',
                        'font-weight': 'nornaml',
                        'margin-top': '10px',
                        'color': titleColor,
                    }), className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{thisMonth}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),
                            html.Div(f"({diff})", style={
                                'font-size': '28px',
                                'font-weight': 'normal',
                                'margin-top': '25px',
                                'color': fontCol,
                            }),
                            ], className='d-flex justify-content-center'),
                    dbc.Row('vs. Previous Month', className='d-flex justify-content-center',
                            style={'color': titleColor, }),
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
                        'color': titleColor,
                    }), className='d-flex justify-content-center'),
                    dbc.Row([
                            html.Div(f"{total}", style={
                                'font-size': '50px',
                                'font-weight': 'bold',
                                'margin': '10px',
                                'color': fontCol,
                            }),

                            ], className='d-flex justify-content-center'),
                    dbc.Row('Last 12 Months', className='d-flex justify-content-center',
                            style={'color': titleColor, }),

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


def getKPILayout():
    return [
        # Main ROW
        dbc.Row(
            # MAIN COL
            dbc.Col(
                [

                    # FIRST ROW
                    dbc.Row(
                        [
                             html.Div(html.Div([
                                    dbc.Row([html.Div(f'Average Customers Per Day', style={
                                        'font-size': '30px',
                                        'font-weight': 'bold',
                                        'margin': '10px',
                                        'color': titleColor,
                                    })]),

                                    dbc.Row([html.Div(getAvgCustsPerDay(),
                                                      style={'font-size': '62px',
                                                             'color': fontCol,
                                                             'margin-top':'10px',
                                                             'font-weight': 'bold', })], className='d-flex justify-content-center ',),


                                    ], style={
                                    'padding-left':'15px',
                                    'padding-right':'15px',
                                    'height':  '300px',
                                    'color': '#008080',
                                     'background-color': bgCol,
                                    'border-radius': '5px',
                                    'font-size': '20px', }),className="mt-2 col-md-6 col-lg-4 col-xl"),
                            
                          
                            html.Div(html.Div([
                                    dbc.Row([html.Div(f'Customer Loyality Rate', style={
                                        'font-size': '30px',
                                        'font-weight': 'bold',
                                        'margin': '10px',
                                        'color': titleColor,
                                    })]),

                                    dbc.Row(

                                        getLoyalCustomersRate(),

                                        className='d-flex justify-content-center ',),
                                    dbc.Row(
                                        dbc.Col(html.Div('This Month vs. Previous Month', style={
                                            'font-size': '24px',
                                            'font-weight': 'normal',
                                            'margin-top': '10px',
                                            'color': titleColor,
                                        }), width=12, className='d-flex justify-content-center')),


                                    ], style={
                                    'padding-left':'15px',
                                    'padding-right':'15px',
                                    'height':  '300px',
                                    'color': '#008080',
                                     'background-color': bgCol,
                                    'border-radius': '5px',
                                    'font-size': '20px', }),className="mt-2 col-md-6 col-lg-4 col-xl"),
                            
                            
                            html.Div(html.Div([
                                    dbc.Row([html.Div(f'Customer Lifetime Value', style={
                                        'font-size': '28px',
                                        'font-weight': 'bold',
                                        'margin': '10px',
                                        'color': titleColor,
                                    })]),

                                    dbc.Row(

                                        getCustomerLifetimeValue(),

                                        className='d-flex justify-content-center',),
                                    dbc.Row(
                                            html.Div('This Month vs. Previous Month', style={
                                            'font-size': '24px',
                                            'font-weight': 'normal',
                                            'margin': '10px',
                                            'color': titleColor,
                                        }), className='d-flex justify-content-center'),



                                    ], style={
                                    'padding-left':'15px',
                                    'padding-right':'15px',
                                    'height':  '300px',
                                    'color': '#008080',
                                     'background-color': bgCol,
                                    'border-radius': '5px',
                                    'font-size': '20px', }),className="mt-2 col-md-6 col-lg-4 col-xl"),
                            
                            
                            html.Div(html.Div([
                                    dbc.Row([html.Div(f'Average Sales Per Customer', style={
                                        'font-size': '28px',
                                        'font-weight': 'bold',
                                        'margin': '10px',
                                        'color': titleColor,
                                    })]),

                                    dbc.Row([html.Div(getAvgSalesPerCust(), 
                                    style={'font-size': '62px', 
                                    'color': fontCol,
                                    'margin-top':'10px',
                                    'font-weight': 'bold', })], className='d-flex justify-content-center',),


                                ], style={
                                    'padding-left':'15px',
                                    'padding-right':'15px',
                                    'height':  '300px',
                                    'color': '#008080',
                                     'background-color': bgCol,
                                    'border-radius': '5px',
                                    'font-size': '20px', }),className="mt-2 col-md-6 col-lg-4 col-xl"),
                            

                        ]
                    ),

                    # SECOND ROW

                    dbc.Row([

                        getCustomerChurn(),
                        getRetentionRate()

                    ]),

                    # THIRD ROWS
                    dbc.Row([

                        getMRR(),
                        getRevenueChurn(),

                    ]),

                ], width=12
            ),
        ),

    ]
