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

item_details = pd.read_csv(
    r'./data/item_details.csv')
items = item_details
items.sort_values(by='Profit', ascending=False, inplace=True)
items = items.head(15)


def topItemsList(limit=5):
    items_list = list(items.index)
    limit_items = []
    i = 0
    for item in items_list:
        if i < limit:
            i += 1
            limit_items.append(item)
    return limit_items


def getCostPriceProfit(value=5):
    itemsReturn = items.head(int(value))
    itemsReturn.sort_values(by='Profit', ascending=False, inplace=True)
    itemsReturn['ItemNo'] = itemsReturn['ItemNo'].astype(str)
    itemName = list(itemsReturn['ItemNo'])
    names = []
    for i in itemName:
        names.append(f"Item {i}")

    itemsReturn['Price'] = itemsReturn['Price'].astype(int)
    # itemsReturn['Cost']=itemsReturn['Cost'].astype(int)
    itemsReturn['Profit'] = itemsReturn['Profit'].astype(int)

    itemPrice = list(itemsReturn['Price'])
    itemCost = list(itemsReturn['Cost'])
    itemProfit = list(itemsReturn['Profit']/10000)
    itemQnty = list(itemsReturn['Qnty']/100)
    # print(names,itemPrice,itemCost,itemProfit)
    return names, itemPrice, itemCost, itemProfit, itemQnty
