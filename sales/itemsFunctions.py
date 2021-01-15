from app import app
from . import general as sales
import plotly.graph_objects as go
import dash_daq as daq
from dash.dependencies import Input, Output
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.BOOTSTRAP]

item_details = pd.read_csv(
    r'./data/compItemCust.csv')
items = item_details

barColorLight='#02B8AC'
barColorDark='#394649'

def getTopItemsList(limit, df):
    limit = int(limit)
    df = pd.DataFrame(df.groupby('ItemNo').TotalProfit.sum())
    df.sort_values(by='TotalProfit', ascending=False, inplace=True)
    df = df.head(limit)
    return list(df.index)


def getTopItemsCost(items, df):
    costs = []
    for item in items:
        cost = df[df['ItemNo'] == item]
        cost = int(sum(cost['TotalCost'])/100)
        costs.append(cost)
    return costs


def getTopItemsProfit(items, df):
    profits = []
    for item in items:
        profit = df[df['ItemNo'] == item]
        profit = int(sum(profit['TotalProfit'])/100)
        profits.append(profit)
    return profits


def getTopItemsSales(items, df):
    sales = []
    # print(df)
    for item in items:
        sale = df[df['ItemNo'] == item]
        # print(sale)
        sale = sum(sale['Qnty'])
        sales.append(sale)
    # print(sales)
    return sales


def getCostPriceProfit(value, month, year):
    itemsReturn = items
    # print(f"{month}{type(month)}"+" "+f"{year}{type(year)}")
    itemsReturn = items[items['Year'] == int(year)]
    itemsReturn = itemsReturn[itemsReturn['Month'] == int(month)]
    itemsReturn.sort_values(by='TotalProfit', ascending=False, inplace=True)
    itemsReturn['ItemNo'] = itemsReturn['ItemNo'].astype(int)
    # GET TOP ITEMS
    top_items = getTopItemsList(value, itemsReturn)
    # print(top_items)
    # print(top_items)
    # print(top_items)
    # GET PROFITS COSTS SALES

    top_items_costs = getTopItemsCost(top_items, itemsReturn)
    top_items_profits = getTopItemsProfit(top_items, itemsReturn)
    top_items_sales = getTopItemsSales(top_items, itemsReturn)
    # NAMING THE ITEMS
    names = []
    for item in top_items:
        names.append("Item "+str(item))
    return names, top_items_sales, top_items_costs, top_items_profits

def getItemGraph(top_items, top_items_sales, top_items_costs, top_items_profits,mainDict):
    fig = go.Figure(
        data=[
            go.Bar(
                marker_color='#009D4E',
                name=f'{mainDict["Cost"]}',
                x=top_items,
                y=top_items_costs),
            go.Bar(
                marker_color="#6AC738",
                name='Sold',
                x=top_items,
                y=top_items_sales),
            go.Line(
                marker_color='rgb(230,131,16)',
                name=f'{mainDict["Profit"]}/100',
                x=top_items,
                y=top_items_profits)
        ])
    fig.update_layout(
        
        title_text='<b></b>',
        plot_bgcolor='rgba(0, 0, 0, 0)',
    )
    return dcc.Graph(figure=fig)


#  MAIN FUNCTIONS


# ITEM DROPDOWN
@app.callback(
    # dash.dependencies.Output('topItemGraph', 'children'),
    dash.dependencies.Output('topItemGraph', 'children'),
    [dash.dependencies.Input('itemsDropDown', 'value')]
)
def itemDropDownCallBack(value):
    selectedMonth = sales.getMonthsList()
    selectedYear = sales.getYearsList()
    print(value)
    (top_items,
     top_items_sales,
     top_items_costs,
     top_items_profits) = getCostPriceProfit(value, selectedMonth[-1], selectedYear[-1])
    return getItemGraph(top_items, top_items_sales, top_items_costs, top_items_profits)
