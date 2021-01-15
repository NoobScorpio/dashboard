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

selectedYear = [2020]
selectedMonth=[0]
selectedItemsDropdown=[15]
selectedItemsCheck=[0]
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']


itemNames = pd.read_csv(
    r'./data/itemNames.csv')
itemNames['ItemNo'] = itemNames['ItemNo'].astype(int)

def getYears():
    i = 0
    menuItems = []
    while i < len(yearsName):
        year = yearsName[i]
        menuItems.append({'label': year, 'value': year})
        i += 1

    return menuItems

def getMonths():
    df=data[data['Year']==selectedYear[-1]]
    months=list(df['Month'].unique())
    print(f" MONTHS : {months}")

    menuItems = []
    menuItems.append({'label': "All", 'value': 0})
    for i in months:
        menuItems.append({'label': monthNames[i-1], 'value': i})


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
        ],
        
    )
    fig.update_layout(
        height=550,
        title=f'<b>Total Items Quarterly ( {selectedYear[-1]} )</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,

    )
    fig.update_traces(textposition='inside', textfont_size=18)
    return dcc.Graph(figure=fig)

def getRegularItemsPerYear(df,month):
    # df = data
    # if month==0:

    
    # df = df[df['Year'] == year]
    if month==0:
        title=f"Regular Items ( All months, {selectedYear[-1]} )"
        months = [g for n, g in df.groupby(
            pd.Grouper(key='InvoiceDate', freq='M'))]
    else:
        title=f"Regular Items ( {monthNames[month-1]}, {selectedYear[-1]} )"
        months = [g for n, g in df.groupby(
            pd.Grouper(key='InvoiceDate', freq='D'))]



    items = list(df['ItemNo'].unique())
    
    for month in months:
        for item in items:
            if item not in list(month['ItemNo']):
                items.remove(item)
    
    return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '28px',
                'font-weight': 'bold',
                # 'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"{len(items)}", style={
            'font-size': '62px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),

    ]

def getMostSoldItem(df,month):
    itemNo=None
    try:  
        if month==0:
            title=f"Most Sold Items ( All months, {selectedYear[-1]} )"
            itemNo=pd.DataFrame(df.groupby('ItemNo').Qnty.sum())
            itemNo=str(itemNo.index[itemNo['Qnty']==max(itemNo['Qnty'])]).split('[')[1].split(']')[0]
            print(type(itemNo))
        else:
            title=f"Most Sold Item ( {monthNames[month-1]}, {selectedYear[-1]} )"
            itemNo=pd.DataFrame(df.groupby('ItemNo').Qnty.sum())
            itemNo=str(itemNo.index[itemNo['Qnty']==max(itemNo['Qnty'])]).split('[')[1].split(']')[0]
            print(type(itemNo))

        name = itemNames[itemNames['ItemNo'] ==
                         int(itemNo)].iloc[0]['AItemName']
        return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '28px',
                'font-weight': 'bold',
                # 'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"{name}", style={
            'font-size': '42px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),]
    except:
            return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '28px',
                'font-weight': 'bold',
                # 'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"No data", style={
            'font-size': '48px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),]

def getNewItems(df,month):
    selectedNewItems=0
    try:
        if month!=0:
            title=f"New Items ( {monthNames[month-1]}, {selectedYear[-1]} )"
            if selectedYear[-1]==2012:
                oldList=data[data['Year']==2012]
                if month==1:
                    oldList=data[data['Month']==1]
                else:
                    oldList=data[data['Month']==month]
            else:
                oldList=data[data['Year']<selectedYear[-1]]
                if month==1:
                    oldList=data[data['Month']==1]
                else:
                    oldList=data[data['Month']==month]
            oldList=list(oldList['ItemNo'].unique())
            newList=list(df['ItemNo'].unique())
            newItems=[]
            for new in newList:
                if new not in oldList:
                    newItems.append(new)
            selectedNewItems=len(newItems)
        else:
            title=f"New Items ( All months, {selectedYear[-1]} )"
            if selectedYear[-1]==2012:
                selectedNewItems=0
            else:
                oldList=data[data['Year']<selectedYear[-1]]

            oldList=list(oldList['ItemNo'].unique())
            newList=list(df['ItemNo'].unique())
            newItems=[]
            for new in newList:
                if new not in oldList:
                    newItems.append(new)
            selectedNewItems=len(newItems)
        return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '28px',
                'font-weight': 'bold',
                # 'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"{selectedNewItems}", style={
            'font-size': '62px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),] 
    except:
        return [
        dbc.Row([
            html.Div(title, style={
                'font-size': '28px',
                'font-weight': 'bold',
                # 'margin': '10px',
                'color':titleColor,
            })
        ]),
        dbc.Row([html.Div(f"No data", style={
            'font-size': '48px',
            'font-weight': 'bold',
        })], className='d-flex justify-content-center mt-5',),] 

def getCashCreditCustomerItemCategory():
    fig = go.Figure(
        data=[
        go.Funnel(
            y = ["Hardware", "Construction", "IT", "Electrical", "Grossary"],
            x = [50, 20.4, 20.6, 11, 5],
            textposition = "inside",
            textinfo = "value",
            opacity = 1, marker = {"color": colors
            },
            connector = {"line": {"color": "black", "dash": "solid", "width": 2}}
            ),
            go.Funnel(
            y = ["Hardware", "Construction", "IT", "Electrical", "Grossary"],
            x = [35, 30, 15, 15, 15],
            textposition = "inside",
            textinfo = "value",
            opacity = 1, marker = {"color": colors},
            connector = {"line": {"color": "black", "dash": "solid", "width": 2}}
            ),
        ],
    )
    fig.update_layout(
        height=550,
        paper_bgcolor='white',
        plot_bgcolor='white',
        title=f'<b>Customers with Items Category</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,

    )
    fig.update_traces(textposition='inside', textfont_size=18)
    # fig.show()
    return dcc.Graph(figure=fig)

def getCashCreditCustomerBrandCategory():
    categories = ['CocaCola','Sony','Intel','AMD','Hitachi','IKEA','Samsung']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=[2000, 1400, 2500, 1600, 1800, 2200, 1900, 1500, 1200, 1600, 1400, 1700],
        name='Credit',
        marker_color=fontColDark
    ))
    fig.add_trace(go.Bar(
        x=categories,
        y=[1900, 1400, 2200, 1400, 1600, 1900, 1500, 1400, 1000, 1200, 1200, 1600],
        name='Cash',
        marker_color=fontCol
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    # fig.show()
    fig.update_layout(
        height=550,
        paper_bgcolor='white',
        plot_bgcolor='white',
        title=f'<b>Credit and Cash Customers with Brands Category</b>',
        title_font_color=titleColor,
        title_font_size=20,
        showlegend=False,

    )
    return dcc.Graph(figure=fig)

def totalItemsPerYear(year,month):
    df = data
    
    if month==0:
        df = df[df['Year'] == year]
    else:
        df = df[df['Year'] == year]
        df=df[df['Month']==month]
    
    quarters = [g for n, g in data[data['Year']==year].groupby(
        pd.Grouper(key='InvoiceDate', freq='Q'))]
    # print(quarters)
    items_list = []
    for i in quarters:
        items_list.append(len(i['ItemNo'].unique()))
    items = len(df['ItemNo'].unique())
    # print(items_list)
    # print(items)
    if month == 0:
        title=f'Total Items ( All months, {selectedYear[-1]} )'
    else:
        title=f'Total Items ( {monthNames[month-1]}, {selectedYear[-1]} )'
    return ([
        dbc.Row(
            [
                dbc.Col(html.Div(title, style={
                        'font-size': '28px',
                        'font-weight': 'bold',
                        # 'margin': '10px',
                        'color':titleColor,
                        })),


            ]
        ),
        dbc.Row(
            html.Div(f"{items}", style={
                'font-size': '62px',
                'font-weight': 'bold',

            }), className='d-flex justify-content-center mt-5',),

    ], 
    getQuarterlyChart(items_list), 
    getRegularItemsPerYear(df,month),
    getMostSoldItem(df,month),
    getNewItems(df,month))


def getTodayItems():
    df = data
    df = df[df['Year'] == max(df['Year'])]
    df = df[df['Month'] == max(df['Month'])]
    df = df[df['Day'] == max(df['Day'])]
    items = len(df['ItemNo'].unique())
    print(items)
    return html.Div(f"{items}", style={
        ' font-size': '36px !important',
        ' font-weight': 'bold !important',
                        ' text-align': 'center',
    })

dropDownStyle = {
    'margin-top': '25px',
    'margin-right': '25px',
    'justify-content': 'end',
    'min-width': '200px',
    'box-shadow': 'none',
    'font-size': '13px',
    'margin-left': '50px',
}

def getTopItemsBarGraph(labels, values, name):
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
                title='<b>Item No</b>',
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

def getTimeLineValueBox(title, value):
    if(type(value)==int or type(value)==float ):
        valint=int(value)
        val=str(value)
        if valint>10000 and valint<100000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
        elif valint>100000 and valint<1000000:
            val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
        elif valint>=1000000:
            val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    else:
        val=value
    return html.Div(
        [
            html.Div(f'{title}', style={
                'color': titleColor,
                'margin': '5px',
                'font-size': '24px',
                "font-weight": "bold"}),

            html.Div(f"{val}", style={
                'margin': '10px',
                'color': fontCol,
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

def getChecksTopItems(check, top):
    if selectedMonth[-1]==0:
        df = data[data['Year']==selectedYear[-1]]
    else:   
        df = data[data['Year']==selectedYear[-1]]
        df=df[df['Month']==selectedMonth[-1]]

    if check == 0:
        name = 'Sales'
        df = pd.DataFrame(df.groupby('ItemNo').TotalPrice.sum()).sort_values(
            by='TotalPrice', ascending=False)
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Item {i}")
        old_values = list(df['TotalPrice'])
        values = []
        for i in old_values:
            values.append(int(i))

    if check == 1:

        # PROFIT
        name = 'Profit'
        df = pd.DataFrame(df.groupby('ItemNo').TotalProfit.sum()
                          ).sort_values(by='TotalProfit', ascending=False)
        print(df)
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Item {i}")
        old_values = list(df['TotalProfit'])
        values = []
        for i in old_values:
            values.append(int(i))
    
    if check == 2:
    
        # Custeomers
        name = 'Customers'
        df = pd.DataFrame(df.groupby('ItemNo').CustomerNo.nunique()
                          ).sort_values(by='CustomerNo', ascending=False)
        print(df)
        df = df.head(top)
        old_labels = list(df.index)
        labels = []
        for i in old_labels:
            labels.append(f"Item {i}")
        old_values = list(df['CustomerNo'])
        values = []
        for i in old_values:
            values.append(int(i))

    topItem=labels[0].split(' ')[1]
    df=data[data['ItemNo']==int(topItem)]
    # print(f"CUIST {topItem}")
    profit=sum(df['TotalProfit'])
    # print(f"PROFIT {profit}")
    sales=sum(df['TotalPrice'])
    # print(f"SALES {sales}")
    return getTopItemsBarGraph(labels, values, name),[
       
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Top Item', str(topItem)),width=12)
                ),
            dbc.Row(
                dbc.Col(getTimeLineValueBox('Sales', float(sales)),width=12)
                
                ),
            dbc.Row(dbc.Col( getTimeLineValueBox('Profit', float(profit)),width=12)
               ),
        
    ]

def getGeneralLayout():
    return [
      
        dbc.Row(
            [
                html.Div('Select Year', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                }),
                dcc.Dropdown(
                    id='totalItemsDropDown', searchable=False, options=getYears(), value=2020, style={
                        'margin': '10px',
                        'width': '250px',
                    }
                ),
                html.Div('Select Month', style={
                    'margin': '15px',
                    'font-size': '28px',
                    'font-weight': 'bold',
                    'color':titleColor,
                }),
                html.Div(id='totalItemsDropDownMonthDiv'),
                
            ], className='d-flex justify-content-center'),

      # FIRST ROW
    # totalItemDropDownValue
    # regularItemsValue
    # mostSoldItemValue
    # newSoldItemValue
        dbc.Row(
           [
               html.Div(html.Div(id='totalItemDropDownValue', style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'padding':'15px',
                   'padding-left':'25px',
                #    'margin-top': '10px',
                   'color': fontCol,
                #    'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ), className='mt-3 col-sm-6 col-md-4 col-lg-4 col-xl'),
               
               html.Div(html.Div(id='regularItemsValue', style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'padding':'15px',
                   'padding-left':'25px',
                #    'margin-top': '10px',
                   'color': fontCol,
                #    'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ), className='mt-3 col-sm-6 col-md-4 col-lg-4 col-xl'),
               
               html.Div(html.Div(id='mostSoldItemValue', style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'padding':'15px',
                   'padding-left':'25px',
                #    'margin-top': '10px',
                   'color': fontCol,
                #    'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ), className='mt-3 col-sm-6 col-md-4 col-lg-4 col-xl'),

                html.Div(html.Div(id='newSoldItemValue', style={
                   'height':  '300px',
                   # 'display': 'flex',
                   # 'width':   '90%',
                   'padding':'15px',
                   'padding-left':'25px',
                #    'margin-top': '10px',
                   'color': fontCol,
                #    'margin': '10px',
                   'background-color': bgCol,
                   'border-radius': '5px',
                   'font-size': '20px', }
               ), className='mt-3 col-sm-6 col-md-4 col-lg-4 col-xl'),

               html.Div(html.Div(
                   [
                       dbc.Row([html.Div(f'Today Items Activity', style={
                           'font-size': '28px',
                           'font-weight': 'bold',
                        #    'margin': '10px',
                           'color':titleColor,
                       })]),

                       dbc.Row([html.Div(getTodayItems(), style={
                        'font-size': '62px',
                        'margin-top': '10px',
                        'font-weight': 'bold', 
                        })], className='d-flex justify-content-center mt-5',),


                   ], style={
                       'padding':'15px',
                       'padding-left':'25px',
                       'height':'300px',
                    #    'margin-top': '10px',
                       'color': fontCol,
                    #    'margin': '10px',
                       'background-color': bgCol,
                       'border-radius': '5px',
                       'font-size': '20px', }
               ), className='mt-3 col-sm-6 col-md-4 col-lg-4 col-xl'),

           ]
        ),

        # SECOND ROW
        dbc.Row([
            
            html.Div(html.Div(id='itemQuraterlyCount'), className='mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-4'),
            
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
                                            id='itemRadioButtons',
                                            options=[
                                                {'label': 'Sales', 'value': 0},
                                                {'label': 'Profit', 'value': 1},
                                                {'label': 'Customers', 'value': 2},

                                            ],
                                            value=selectedItemsCheck[-1],
                                            labelStyle={
                                                'display': 'inline-block',
                                                'margin-left': '15px',
                                                'margin-top': '25px',
                                                'font-size': '18px',
                                                'font-weight': 'bold',
                                                'color': titleColor,
                                            }
                                        ),],id='itemRadioButtonsDiv'
                                        ),
                                        html.Div(
                                            [dcc.Dropdown(id='topItemsDropdown', searchable=False, options=[
                                            {'label': 'Top 10 Items',
                                                'value': 10},
                                            {'label': 'Top 15 Items',
                                                'value': 15},
                                            {'label': 'Top 20 Items',
                                                'value': 20},
                                        ], value=selectedItemsDropdown[-1])],id='topItemsDropdownDiv', style=dropDownStyle)

                                    ], width=12, className='d-flex justify-content-end')

                                ]
                            ),

                            dbc.Row(
                                dbc.Col(
                                    id='itemRadioValue'
                                )
                            )

                        ],width=9,
                    ),
                    dbc.Col(id='itemRadioValueBoxes',width=3),
                    ]
                ), style={'background-color': 'white'}), className='mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-8'),
        ], className='mt-2'),
        
        # THIRD ROW
        dbc.Row(
            [
               html.Div( 
                   html.Div(getCashCreditCustomerItemCategory())
                   , className='mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-4'),
                
                html.Div(
                    html.Div(getCashCreditCustomerBrandCategory(), 
                style={'background-color': 'white'})
                , className='mt-3 col-sm-12 col-md-12 col-lg-6 col-xl-8'),
            ], className='mt-2'
        ),
    ]

# MAIN CALLBACK
@app.callback(
    Output("totalItemsDropDownMonthDiv", "children"),
    [Input("totalItemsDropDown", "value"),],
)
def render_tab_content(value):
    if value==None:
        value=2020
    selectedYear.append(value)
    return dcc.Dropdown(
                    id='totalItemsDropDownMonth', 
                    searchable=False, 
                    options=getMonths(), 
                    value=selectedMonth[-1], 
                    style={
                        'margin': '10px',
                        'width': '250px',
                    }
                )

@app.callback(
    Output("totalItemDropDownValue", "children"),
    Output("itemQuraterlyCount", "children"),
    Output("regularItemsValue", "children"),
    Output("mostSoldItemValue", "children"),
    Output("newSoldItemValue", "children"),
    [Input("totalItemsDropDownMonth", "value")])
def itemMonthDropFUnction(value):
    if value == None:
        value = 0
    selectedMonth.append(value)

    selectedMonth.append(value)
    total, quarter, regular,mostItem,newItems = totalItemsPerYear(selectedYear[-1],value)
    # graph,boxes=getChecksTopItems(0, 15)
    return total, quarter, regular, mostItem,newItems

# RADIO CALLBACK
@app.callback(
    Output("itemRadioValue", "children"),
    Output("itemRadioValueBoxes", "children"),
    [Input("itemRadioButtons", "value"), Input("topItemsDropdown", "value"),Input("totalItemsDropDownMonth", "value") ],
)
def checkTopCallback(value, value2,value3):
    print('INSIDE CHECK')
    if value == None:
        value = 0
    if value3==None:
        value3=0
    selectedItemsCheck.append(value)
    selectedItemsDropdown.append(value2)
    return getChecksTopItems(value, value2)





