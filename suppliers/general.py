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
selectedSupDropdown=[15]
selectedSupplier=[1]
selectedSupCheck=[0]

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

def getFirstRowStyle(title):
    return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '24px',
                'font-weight': 'bold',
                'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"255", style={
            'font-size': '60px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),

    ]

def getQuarterlyChart(quarters):
    j = 1
    labels = ["Q1","Q2","Q3","Q4",]
    values = [50,100,150,200]
    # for i in quarters:

    #     labels.append(f"Quarter {j}")

    #     values.append(int(i))
    #     j += 1

    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(
        data=[
            go.Pie(

                labels=labels,
                values=values,
                hole=.5,
                marker_colors=colors

            )
        ],
        
    )
    fig.update_layout(
        height=550,
        title=f'<b>Total Items Quarterly ( {selectedYear[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,

    )
    return dcc.Graph(figure=fig)


def getFirstRowData(year,month,sup):
    if month==0:
        title=f"( All months, {selectedYear[-1]}, S {sup} )"
    else:
        title=f"( {monthNames[month-1]}, {selectedYear[-1]}, S {sup} )"
    print("RETURNING STUFF")
    print(f"THIS IS TITLE , {title}")
    print("RETURNING STUFF")
    return (
        getFirstRowStyle("Total "+str(title)),
        getQuarterlyChart('items_list'), 
        getFirstRowStyle("Profit "+str(title)),
        getFirstRowStyle("Quantity "+str(title)),
        getFirstRowStyle("Best Item "+str(title)),
        )



def getGeneralLayout():
    print('INSIDE LAYOUT')
    # return "LAYOUT"
    return [
        # YEAR MONTH SUPPLIER ROW
        dbc.Row(
            [
                html.Div([html.Div('Select Year', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                }),
                dcc.Dropdown(
                    id='supYearDropDown', searchable=False, options=getYears(), value=2020, style={
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
                html.Div(id='supYearMonthDropDownDiv', style={
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
                html.Div(id='supYearMonthNoDiv', style={
                        'margin': '10px',
                        'width': '250px',
                    })],className="col-4"),
                
            ]),
    
    # FIRST ROW supTotalSales    supTotalProfit     supTotalQuantity     supMostItem
    
        dbc.Row(
           [
               html.Div(html.Div(id='supTotalSales', style={
                   'height':  '300px',
                   'padding':'15px',
                   'color': fontCol,
                   'background-color': bgCol,
                   'border-radius': '5px',
                  
                   }
               ),className="mt-2 col-sm-6 col-md-6 col-lg-3 col-xl-3"),

               html.Div(html.Div(id='supTotalProfit', style={
                   'height':  '300px',
                   'padding':'15px',
                   'color': fontCol,
                   'background-color': bgCol,
                   'border-radius': '5px',
                  
                   }
               ),className="mt-2 col-sm-6 col-md-6 col-lg-3 col-xl-3"),

               html.Div(html.Div(id='supTotalQuantity', style={
                   'height':  '300px',
                   'padding':'15px',
                   'color': fontCol,
                   'background-color': bgCol,
                   'border-radius': '5px',
                
                   }
               ),className="mt-2 col-sm-6 col-md-6 col-lg-3 col-xl-3"),

               html.Div(html.Div(id='supMostItem', style={
                   'height':  '300px',
                   'padding':'15px',
                   'color': fontCol,
                   'background-color': bgCol,
                   'border-radius': '5px',
                 
                   }
               ),className="mt-2 col-sm-6 col-md-6 col-lg-3 col-xl-3"),

               
               
           ]
        ),

        # SECOND ROW
        dbc.Row([
            
           html.Div([html.Div(id='supQuraterlyCount')],className="mt-2 col-sm-12 col-md-12 col-lg-4 col-xl-4"),
            
            html.Div(html.Div(
                dbc.Row(
                    [
                        dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col([
                                        # html.Div('Top Items'),
                                        html.Div(
                                            [dcc.RadioItems(
                                            id='supRadioButtons',
                                            options=[
                                                {'label': 'Sales', 'value': 0},
                                                {'label': 'Profit', 'value': 1},
                                                {'label': 'Customers', 'value': 2},

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
                                        ),],id='supRadioButtonsDiv'
                                        ),
                                        html.Div(
                                            [dcc.Dropdown(id='supTopSupsDropdown', searchable=False, options=[
                                            {'label': 'Top 10 Items',
                                                'value': 10},
                                            {'label': 'Top 15 Items',
                                                'value': 15},
                                            {'label': 'Top 20 Items',
                                                'value': 20},
                                        ], value=15)],id='supTopSupsDropdownDiv', style=dropDownStyle)

                                    ], width=12, className='d-flex justify-content-end')

                                ]
                            ),

                            dbc.Row(
                                dbc.Col(
                                    id='supRadioValue'
                                    # dcc.Graph(),width=12
                                )
                            )

                        ],width=9,
                    ),
                    dbc.Col(id='supRadioValueBoxes',width=3),
                    ]
                ), style={'background-color': 'white'}),className="mt-2 col-sm-12 col-md-12 col-lg-8 col-xl-8"),
        ],),

    ]
def getTopSupBarGraph(labels, values, name,sup):
    labels=["Supplier 1","Supplier 2","Supplier 3","Supplier 4","Supplier 5","Supplier 6"]
    values=[9,8,7,6,5,4]
    
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
                title='<b>Supplier No</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                     color=titleColor
                )
            ),
            yaxis=dict(
                title=f'<b>Check</b>',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=18,
                     color=titleColor
                )
            )
        )
    )
    if selectedMonth[-1]==0:
        title= f'<b>Top Items ( All months, {selectedYear[-1]} )</b>'
    else:
        title= f'<b>Top Items ( {monthNames[selectedMonth[-1]-1]},{selectedYear[-1]} )</b>'
    fig.update_layout(
        title_text=title,
        title_font_size=24,
        title_font_color=titleColor,
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1,  # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(figure=fig)

def getChecksTopSupplier(check, top,sup):

    return getTopSupBarGraph('labels', 'values', 'name',sup),[
       
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Top Suppliers', '564'),width=12)
                ),
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Sales', '34522224'),width=12)
                
                ),
            dbc.Row(dbc.Col( getTimeLineValueBox('Quantity', '545463'),width=12)
               ),
        
    ]
def getTimeLineValueBox(title, value):
    return html.Div(
        [
            html.Div(f'{title}', style={
                'color': titleColor,
                'margin': '5px',
                'font-size': '24px',
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
            'border': '1px solid #ebebeb',
        }
    )


# RADIO CALLBACK
@app.callback(
    Output("supRadioValue", "children"),
    # Output("supRadioValueBoxes", "children"),
    [Input("supRadioButtons", "value"), Input("supTopSupsDropdown", "value"), ],
)
def checkTopCallback(value, value2):
    print('INSIDE CHECK')
    if value == None:
        value = 0
    selectedSupDropdown.append(value2)
    selectedSupCheck.append(value)
    return getChecksTopSupplier(value, value2,selectedSupplier[-1])



# MAIN CALLBACK
@app.callback(
    Output("supYearMonthDropDownDiv", "children"),
    [Input("supYearDropDown", "value"),],
)
def render_tab_content(value):
    if value==None:
        value=2020
    selectedYear.append(value)
    print("Year APPENDIND ")
    return dcc.Dropdown(
                    id='supYearMonthDropDown', 
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
    Output("supYearMonthNoDiv", "children"),
    [Input("supYearMonthDropDown", "value")])
def itemMonthDropFUnction(value):
    if value == None:
        value = 1
    return dcc.Dropdown(
                    id='supYearMonthNo', 
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
    Output("supTotalSales", "children"),
    Output("supQuraterlyCount", "children"),
    Output("supTotalProfit", "children"),
    Output("supTotalQuantity", "children"),
    Output("supMostItem", "children"),
    # Output("supRadioValue", "children"),
    Output("supRadioValueBoxes", "children"),

    [Input("supYearMonthNo", "value")])
def itemMonthSupDropFUnction(value):
    if value == None:
        value = 0
    selectedSupplier.append(value)
    
    print("MIONTH APPENDIND ")
    total,qurater, profit, qnty,most= getFirstRowData(selectedYear[-1],selectedMonth[-1],value)
    graph,boxes=getChecksTopSupplier(0, 15,value)
    print("REURNING MONTH DROPDOWN APPENDIND SUPS ")
    return total,qurater, profit, qnty,most,graph,boxes




