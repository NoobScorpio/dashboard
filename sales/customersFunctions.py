from . import general as sales
from app import app
import plotly.graph_objects as go
import dash_daq as daq
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
# import sales
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.BOOTSTRAP]

cust = pd.read_csv(
    r'./data/Sells(C).csv')
cust['InvoiceDate'] = pd.to_datetime(cust['InvoiceDate'])


def getTopCusts(limit, df):
    limit = int(limit)
    df = pd.DataFrame(df.groupby('CustomerNo').Total.sum())
    df.sort_values(by='Total', ascending=False, inplace=True)
    df = df.head(limit)
    return list(df.index)


def getTopCustTotal(custs, df):
    costs = []
    for cust in custs:
        cost = df[df['CustomerNo'] == cust]
        cost = int(sum(cost['Total'])/100)
        costs.append(cost)
    return costs


def getTopCustomer(value, month, year,mainDict):
    topCusts = cust[cust['Year'] == int(year)]
    topCusts = cust[cust['Month'] == int(month)]
    topCusts['CustomerNo'] = topCusts['CustomerNo'].astype(int)
    topCusts.sort_values(by='Total', ascending=False, inplace=True)

    # GET TOP CUSTOMERS
    top_custs = getTopCusts(value, topCusts)
    # print(top_custs)
    names = []
    for custr in top_custs:
        names.append(f"{mainDict['Customer']} "+str(custr))
    top_cust_total = getTopCustTotal(top_custs, topCusts)
    # print(names,top_cust_total)
    return getCustomerGraph(names, top_cust_total)


def getCustomerGraph(names, values):
    fig = go.Figure(
        data=[
            go.Bar(
                marker_color='#6AC738',
                name='LA Zoo',
                x=values,
                y=names,
                orientation='h',

            )
        ], )
    fig.update_layout(
        title_text='<b></b>',
        plot_bgcolor='rgba(0, 0, 0, 0)',)
    return dcc.Graph(figure=fig)


# Main

selectedMonth = [1]
selectedYear = [2012]


# CUSTOMER DROPDOWN

@app.callback(
    # dash.dependencies.Output('topItemGraph', 'children'),
    dash.dependencies.Output('getCustomerGraph', 'children'),
    [dash.dependencies.Input('custsDropDown', 'value')]
)
def itemDropDownCallBack(value):
    selectedMonth = sales.getMonthsList()
    selectedYear = sales.getYearsList()
    return getTopCustomer(value, selectedMonth[-1], selectedYear[-1])
