import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

itemDetails = None
timelineItems = None


def itemData():
    global itemDetails, timelineItems
    itemDetails = pd.read_csv(
        r'./data/Sells_Detail.csv')
    # TIMELINE ITEMS
    timelineItems = itemDetails
    timelineItems = timelineItems[timelineItems['ItemNo'] != '.']
    timelineItems['ItemNo'] = timelineItems['ItemNo'].astype(int)
    # data = pd.read_csv(
    # r'D:\\WORK\\JMM TECH PVT\\BUSSINESS INTELLIGENCE\\Data\\NEW\\items.csv')
    # data = data[data['ItemNo'] != '.']
    return data


data = itemData()
itemList = data['ItemNo'].unique().tolist()
opts = []
for i in itemList:
    opts.append({'label': i, 'value': i})


def namesData():
    names = pd.read_csv(
        r'D:\\WORK\\JMM TECH PVT\\BUSSINESS INTELLIGENCE\\DashBoard\\Data\\items.csv')
    names.drop_duplicates(inplace=True)
    names = names[names['ItemNo'] != '.']
    names = names.fillna(999999)
    return names


sums = pd.DataFrame(data.groupby('InvoiceDate').Qnty.sum())
fig = px.line(sums, x=sums.index, y="Qnty")


def func():
    return html.Div(children=[
        html.H1(children='Select Item Below', style={
            'font-size': '28px',
            'textAlign': 'center',

        }),

        html.Div(
            dcc.Dropdown(
                id='dropdown',
                options=opts,
                value='2211'
            ), style={
                'margin': 'auto',
                'width': '200px',
                'textAlign': 'center',
                'padding': '15px',
            },
        ),
        html.Div(id='dd-output-container', style={
            'textAlign': 'center',
            'color': 'black'
        }),
        html.Div(id='', style={
            'textAlign': 'center',
            'color': 'black'
        }),
    ])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    names = namesData()
    items = itemData()
    names['ItemNo'] = names['ItemNo'].astype(int)
    items = items[items['ItemNo'] == value]
    # print(items)

    names = names[names['ItemNo'] == value]
    name = names['AItemName']
    nowName = ''
    for i in name:
        nowName = i
    return html.Div(
        dcc.Graph(
            id='bar chart',
            figure={
                "data": [
                    {
                        "x": items["InvoiceDate"],
                        "y": items["Qnty"],
                        "type": "line",
                        "marker": {"color": "#0074D9"},
                    }
                ],
                "layout": {
                    'title': f'{nowName} TimeLine',
                    "xaxis": {"title": "Quantity"},
                    "yaxis": {"title": "InvoiceDate"},
                },
            },
        )
    )

#######################################################################
######################################################################
#####################################################################
###################  ITEMS COST PRICE PROFIT TIMELINE################


def itemTimelineGraph(itemNo):
    global timelineItems
    item = timelineItems[timelineItems['ItemNo'] == int(itemNo)]
    cost = int(timelineItems['Cost'].mean())
    price = int(timelineItems['Price'].mean())
    profit = price-cost
    item = pd.DataFrame(item.groupby('InvoiceDate').Qnty.sum())
    return (getTimelineGraph(item, itemNo), getitemCost(cost), getitemPrice(price), getitemProfit(profit))


def getTimelineGraph(item, itemNo):
    return dcc.Graph(
        id='cMonthGraph',
        figure={
            "data": [
                {
                    "x": item.index,
                    "y": item["Qnty"],

                    "type": "line",
                            "marker": {"color": "rgba(137, 184, 80, 1)"},
                            "name": "Sales",
                            'fill': 'tozeroy',
                            'fillcolor': 'rgba(193, 255, 117, 0.1)',
                            'line': {'shape': 'spline', 'smoothing': 1}
                },
                {
                    "x": item.index,
                    "y": item["Qnty"],
                    "type": "line+marker",
                            "name":"Goal",
                            # "marker": {
                            #     "line":{
                            #         'color':'white',
                            #         'width':5
                            #     },
                            #     "color": "rgba(255, 196, 0, 1)",
                            #     "size":10,

                            #     },
                }

            ],
            "layout": {
                'title': {
                    'text': f"<b>ItemNo {itemNo}</b>",
                            'y': 0.9,
                            'x': 0.07,
                            'xanchor': 'left',
                            'yanchor': 'top'},
                'font': {'size': '16px', 'color': 'black'},
                'legend': {

                    'x': '0.45',
                    'y': '1.25',
                    'orientation': 'h'
                },

                # "width":1000,
                # "height":200
            },
        },
    )


def getitemCost(cost):
    return html.Div(
        [
            html.Div('Cost', style={
                'margin': '10px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{int(cost)}", style={
                'margin': '10px',
                'color': '#89B850',
                'font-size': '28px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ], style={
            'margin': '20px',
            'height': '120px',
            'width': '300px',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'border': '1px solid #ebebeb', }
    )


def getitemPrice(price):
    return html.Div(
        [
            html.Div('Price', style={
                'margin': '10px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{int(price)}", style={
                'margin': '10px',
                'color': '#89B850',
                'font-size': '28px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ], style={
            'margin': '20px',
            'height': '120px',
            'width': '300px',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'border': '1px solid #ebebeb', }
    )


def getitemProfit(profit):
    return html.Div(
        [
            html.Div('Margin', style={
                'margin': '10px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{int(profit)}", style={
                'margin': '10px',
                'color': '#89B850',
                'font-size': '28px',
                "font-weight": "bold",
                'justify-content': 'center',
                'text-align': 'center'}),
        ], style={
            'margin': '20px',
            'height': '120px',
            'width': '300px',
            'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
            'border': '1px solid #ebebeb', }
    )
