from . import salesPage as cP
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
import charts
from . import itemsFunctions as itemsF
from . import customersFunctions as cust

headerEnDict=cP.headerEnDictGen
headerArDict=cP.headerArDictGen

mainDict=headerEnDict
lastLang=[mainDict]
titleColor=cP.titleColor
fontCol=cP.fontCol
fontColDark=cP.fontColDark
bgCol=cP.bgCol
colors=cP.Colors

# ##############################
# SELECTED MONTH VARIABLE
#  ##########################
nowMonth = None

# SELLS DATA
sales = pd.read_csv(
    r'./data/compItemCust.csv')
sales.drop_duplicates(inplace=True)
sales.drop(columns=['Unnamed: 0'], inplace=True)
sales['InvoiceDate'] = pd.to_datetime(sales['InvoiceDate'])
months = [g for n, g in sales.groupby(pd.Grouper(key='InvoiceDate', freq='M'))]
years = [g for n, g in sales.groupby(pd.Grouper(key='InvoiceDate', freq='Y'))]
selectedYear = years[-1]
selectedMonth = [g for n, g in selectedYear.groupby(
    pd.Grouper(key='InvoiceDate', freq='M'))]

# ITEMS DATA
# TOTAL ITEMS
itemsSold = sales
itemsSold['InvoiceDate'] = pd.to_datetime(itemsSold['InvoiceDate'])
itemMonths = [g for n, g in itemsSold.groupby(
    pd.Grouper(key='InvoiceDate', freq='M'))]
itemYears = [g for n, g in itemsSold.groupby(
    pd.Grouper(key='InvoiceDate', freq='Y'))]
selectedItemYear = itemYears[-1]
selectedItemMonth = [g for n, g in selectedItemYear.groupby(
    pd.Grouper(key='InvoiceDate', freq='M'))]

# MOST SOLD ITEM
itemDetails = pd.read_csv(
    r'./data/Sells_Detail.csv')
itemDetails['InvoiceDate'] = pd.to_datetime(itemDetails['InvoiceDate'])
itemMostYears = [g for n, g in itemDetails.groupby(
    pd.Grouper(key='InvoiceDate', freq='Y'))]
selectedTotalItemsYear = itemMostYears[-1]
selectedTotalItemsMonth = [g for n, g in selectedTotalItemsYear.groupby(
    pd.Grouper(key='InvoiceDate', freq='M'))]


# ITEM NAMES
itemNames = pd.read_csv(
    r'./data/itemNames.csv')
itemNames['ItemNo'] = itemNames['ItemNo'].astype(int)
# TIMELINE ITEMS
# timelineItems=itemDetails
# timelineItems=timelineItems[timelineItems['ItemNo']!='.']
# timelineItems['ItemNo']=timelineItems['ItemNo'].astype(int)

monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
yearsName = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]


# ############################## #
#     MOST SOLD ITEM IN MONTH
# ############################## #


def mostItemSold(month=selectedTotalItemsMonth[-1]):
    items = pd.DataFrame(month.groupby('ItemNo').Qnty.sum())
    mostSoldItem = items[items['Qnty'] == max(items['Qnty'])].index[0]
    name = itemNames[itemNames['ItemNo'] == mostSoldItem].iloc[0]['AItemName']
    return [
        html.Span(f"{name}", style={'font-size': '16px', 'color': '#89B850'}),
    ]

# ########################## #
#     CURRENT MONTH PLOT
# ########################## #


# ########################## #
#     YEAR MONTH PLOT + HELPER FUNCTIONS
# ########################## #


def weeksEval(month):
    # print('EVALUATING MONTH')
    mainDict=lastLang[-1]
    weeks = [g for n, g in month.groupby(
        pd.Grouper(key='InvoiceDate', freq='W'))]
    weeks_list = []
    for week in weeks:
        weeks_list.append(pd.DataFrame(
            week.groupby('InvoiceDate').Total.sum()))
    weeks_sum_dict = {}
    i = 1
    for week in weeks_list:
        weeks_sum_dict[f"{mainDict['Week']} {i}"] = week['Total'].sum()
        i += 1
    weeks_sum_dict = OrderedDict(
        sorted(weeks_sum_dict.items(), key=itemgetter(1)))
    iterator = iter(weeks_sum_dict.items())
    # print('RETURNING EVAL MONTH')
    return list(iterator)
#######################################


def selectedMonthGraph(nowMonth, title):
    # print('INSIDE SEECTED MONTH GRAPH')
    mainDict=lastLang[-1]
    nowMonth['Max'] = max(nowMonth['Total'])
    fig = go.Figure(
        data=[
            go.Line(
                x=nowMonth.index,
                y=nowMonth['Max'],
                line=dict(color='#62B102', width=1,
                          dash='dash'),
                name=f"{mainDict['Max']}",
            ),

            go.Line(
                x=nowMonth.index,
                y=nowMonth['Total'],
                marker_color='#6AC738',
                name=f"{mainDict['Sales']}",
                fill='tozeroy',
                fillcolor='rgba(204, 235, 194,0.2)',
                # line=dict(shape='spline', smoothing=1),

            ),

            go.Line(
                x=nowMonth.index,
                y=nowMonth['Mean'],
                line=dict(color='orange', width=1,
                          dash='dash'),
                name=f"{mainDict['Average']}",
            ),


        ],
        layout=go.Layout(
            xaxis=dict(
                title=f'{mainDict["Date"]}',
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            ),
            margin= dict(
                   l= 60,
                   r= 15,
                   b= 0,
                   t= 15,
                   pad= 0
                 ),
            yaxis=dict(
                title=f"{mainDict['Sales']}",
                titlefont=dict(
                    # family='Courier New, monospace',
                    size=16,
                    # color='#7f7f7f'
                )
            )
        )
    )
    fig.update_layout(
         title={
        'text': f'',
        'y':0.85,
        'x':0.15,
        'xanchor': 'center',
        'yanchor': 'top'},
        title_font_size=20,
       autosize=True,
        # bargap=0.15, # gap between bars of adjacent location coordinates.
        # bargroupgap=0.1, # gap between bars of the same location coordinate.
        paper_bgcolor='white',
        plot_bgcolor='white',
    )
    return dcc.Graph(
        id='nowMonthGraph',
        figure=fig

    )

####################################



####################################



####################################


def selectedMonthTopCustomer(cust):
    mainDict=lastLang[-1]
    return getboxDiv(cust, f'{mainDict["Top Customer"]}')

####################################


def selectedMonthTotalSale(totalSale):
    mainDict=lastLang[-1]
    valint=int(totalSale)
    print(f"TOTAL SALES : {valint}")
    val=str(totalSale)
    if valint>10000 and valint<100000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif valint>100000 and valint<1000000:
        val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif valint>=1000000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    return getboxDiv(val, f'{mainDict["Total Sales"]}')

####################################
#


def selectedMonthTotalItems(selectedTotalItems):
    mainDict=lastLang[-1]
    valint=int(sum(selectedTotalItems['Qnty']))
    print(f"TOTAL ITEMS : {valint}")
    val = str(sum(selectedTotalItems['Qnty']))
    if valint>10000 and valint<100000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif valint>100000 and valint<1000000:
        val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif valint>=1000000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    return getboxDiv(val, f'{mainDict["Items Sold"]}')

####################################


def selectedMostItemSold(selectedMostItem):
    mainDict=lastLang[-1]
    if selectedMostItem.empty:
        return getboxDiv('NoData', 'Best Item')
    items = pd.DataFrame(selectedMostItem.groupby('ItemNo').Qnty.sum())
    mostSoldItem = items[items['Qnty'] == max(items['Qnty'])].index[0]
    # print(mostSoldItem)
    name = itemNames[itemNames['ItemNo'] ==
                     int(mostSoldItem)].iloc[0]['AItemName']
    
    return getboxDiv(name, f'{mainDict["Best Item"]}')

####################################


def selectedMostProfit(profit):
    mainDict=lastLang[-1]
    valint=int(profit)
    print(f"TOTAL PROFIT : {valint}")
    val = str(profit)
    if valint>10000 and valint<100000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'K'
    elif valint>100000 and valint<1000000:
        val=val[0:1]+val[1:2]+val[2:3]+'.'+val[3:4]+'K'
    elif valint>=1000000:
        val=val[0:1]+val[1:2]+'.'+val[2:3]+'M'
    return getboxDiv(val, f'{mainDict["Profit"]}')

####################################


def getboxDiv(name, title):
    mainDict=lastLang[-1]
    if title=="Best Item" or title==mainDict['Best Item']:
        size='24px'
    else:
        size='40px'
    
    return html.Div(
            [
                html.Div(f'{title}', style={
                    'color':"black",
                    'margin-top': '15px',
                    'margin-left': '15px',
                    'margin-right': '15px',
                    'margin-bottom': '0px',
                    'font-size': '24px',
                    # "font-weight": "bold"
                    }),

                html.Div(f"{name}", style={
                    'margin': '5px',
                    'color': fontCol,
                    'font-size': f'40px',
                    "font-weight": "bold",
                    'justify-content': 'center',
                    'text-align': 'center'}),
            ],
            style={
               
                'height': '170px',
                'background-color': 'white',
                'min-width': '200px', 
                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                'border': '1px solid #ebebeb', }
        )


# ################################# #
#     CURRENT MONTH WEEKLY PLOT
# ################################# #

# ########################## #
#     BEST WEEK
# ########################## #


def bestWeek(month=months[-1]):
    # month=months[-1]
    weeks = [g for n, g in month.groupby(
        pd.Grouper(key='InvoiceDate', freq='W'))]
    bestWeek = []
    for week in weeks:
        bestWeek.append(week['Total'].sum())
    b = bestWeek.index(max(bestWeek))
    # sale = max(bestWeek)  
    if b+1 == 1:
        return returnStyle(f"{b+1}st")
    if b+1 == 2:
        return returnStyle(f"{b+1}nd")
    if b+1 == 3:
        return returnStyle(f"{b+1}rd")
    if b+1 == 4:
        return returnStyle(f"{b+1}th")
    if b+1 == 5:
        return returnStyle(f"{b+1}th")


def returnStyle(val):
    return [
        html.Span(f"{val}", style={'font-size': '28px', 'color': '#89B850'}),
        html.Span(f" week", style={'font-size': '18px', 'color': '#89B850'}),
    ]
# ########################## #
#     LOW WEEK
# ########################## #


def lowWeek(month=months[-1]):
    # month=months[-1]
    weeks = [g for n, g in month.groupby(
        pd.Grouper(key='InvoiceDate', freq='W'))]
    lowWeek = []
    for week in weeks:
        lowWeek.append(week['Total'].sum())
    b = lowWeek.index(min(lowWeek))
    # sale = min(lowWeek)
    if b+1 == 1:
        return returnStyle(f"{b+1}st")
    if b+1 == 2:
        return returnStyle(f"{b+1}nd")
    if b+1 == 3:
        return returnStyle(f"{b+1}rd")
    if b+1 == 4:
        return returnStyle(f"{b+1}th")
    if b+1 == 5:
        return returnStyle(f"{b+1}th")

# ########################## #
#     MONTHS DROPDOWN ITEMS
# ########################## #


def getMonths():
    df=sales[sales['Year']==selectedYear[-1]]
    dfMonths=list(df['Month'].unique())
    # i = 0
    menuItems = []
    for i in dfMonths:
        menuItems.append(dbc.DropdownMenuItem(
            str(monthNames[i-1]), id=f"{str(monthNames[i-1])}"))
     
    # while i < len(monthNames):
    #     menuItems.append(dbc.DropdownMenuItem(
    #         str(monthNames[i]), id=f"{str(monthNames[i])}"))
        # menuItems.append(dbc.DropdownMenuItem(divider=True),)
        # print(monthNames[i])
        # i += 1
    # print(f"THIS IS MONTH ARRAY LENGTH {len(menuItems)}")
    return menuItems


def getMonthsDCC():
    mainDict=lastLang[-1]
    df=sales[sales['Year']==selectedYear[-1]]
    months=list(df['Month'].unique())
    print(f" MONTHS : {months}")

    menuItems = []
    # menuItems.append({'label': "", 'value': 0})
    for i in months:
        menuItems.append({'label': mainDict[monthNames[i-1]], 'value': i})


    return menuItems
# ########################## #
#     YEARS DROPDOWN ITEMS
# ########################## #


def getYears():
    i = 0
    menuItems = []
    while i < len(yearsName):
        menuItems.append(dbc.DropdownMenuItem(
            str(yearsName[i]), id=f"{str(yearsName[i])}"))
        i += 1

    return menuItems

####################################


def getYearsDCC():
    i = 0
    menuItems = []
    while i < len(yearsName):
        year = yearsName[i]
        # print(f"YEAR  : {year}")
        menuItems.append({'label': year, 'value': year})
        i += 1

    return menuItems


# MAIN FUNCTIONS


def salesGeneralTab():
    return [
        dbc.Row(
            dbc.Col([
                dbc.Row([html.Div(id='change-lang-div'),
                    dcc.Dropdown(
                            id='sales-gen-lang-dropdown',
                            options=[
                                {'label': 'English', 'value': 'En'},
                                {'label': 'Arabic', 'value': 'Ar'}
                            ],
                            value='En',
                            searchable=False,
                            style={'width': '150px',    'height': '20px',}
                                     )])
            ],width=12,className="d-flex justify-content-end")
        ),
        dbc.Row([
                dbc.Col(
                    id='selectedMonthTotalSale',
                 className="col-sm-4 mt-3 col-md-4 col-lg-4 col-xl"
                 ),
                dbc.Col(
                    id="selectedMonthTotalItems",
               className="col-sm-4 mt-3  col-md-4 col-lg-4 col-xl"
                ),
                dbc.Col(
                id='selectedMostItemSold',
                className="col-sm-4 mt-3  col-md-4 col-lg-4 col-xl"
                 ),
                dbc.Col(
                   id='selectedMonthProfit',
                className="col-lg-6 col-xl mt-3 "
                 ),
                dbc.Col(
                    id='selectedMonthTopCustomer',
                className="col-lg-6 col-xl mt-3"
                ),
            ]),
        dbc.Row(selectedMonthyearGraphs(),),
        dbc.Row(salesBottomPlots(), className='mt-3'),
    ]

@app.callback(
    
    dash.dependencies.Output('change-lang-div', 'children'),
    dash.dependencies.Output('select-year-div', 'children'),
    dash.dependencies.Output('select-month-title-div', 'children'),
    dash.dependencies.Output('select-year-title-div', 'children'),
    [dash.dependencies.Input('sales-gen-lang-dropdown', 'value')])
def update_output(value):
    if value=='En':
        mainDict=headerEnDict
        lastLang.append(mainDict)
    if value=='Ar':
        mainDict=headerArDict
        lastLang.append(mainDict)
        print(f"INSIDE Arabic {mainDict['Top Items']}")
    return mainDict['Change Language'],dcc.Dropdown(
                                         id='dropdown1',
                                         options=getYearsDCC(),
                                         value=2020,
                                         searchable=False,
                                         style={'width': '150px',    'height': '20px',}
                                     ),f"{mainDict['Select Month']}",f"{mainDict['Select Year']}"
selectedMonth = [1]
selectedYear = [2012]


def getMonthsList():
    return selectedMonth


def getYearsList():
    return selectedYear


dropDownStyle = {
    'justify-content': 'end',
    'align-content': 'center',    'text-align': 'center',
    'border': '1px solid #89B850',
    'color': '#89B850',
    'appearance': 'none',
    'min-width': '100px',
    'box-shadow': 'none',
    'font-size': '13px',

}

def salesBottomPlots():
    return [
        # FIRST COL
        html.Div(
            [
                html.Div(
                    [

                        dbc.Row([

                            dbc.Col(html.Div(id="topItemsTitle", style={
                                            'font-size':'24px',
                                            'margin-top':'30px',
                                            'margin-left':'50px',
                                            'font-weight':'bold'
                              
                            }), className=" mr-5 d-flex justify-content-start"), 

                            dbc.Col(html.Div(
                                id='itemsDropDownDiv', style={
                                    'justify-content': 'end',
                                    'align-content': 'center',    
                                    'text-align': 'center',
                                 
                                  
                                    'min-width': '100px',
                                    
                                    'margin-top': '15px',
                                    'margin-bottom': '30px',
                                    ' font-size': '13px',
                                },), className=" mr-5 d-flex justify-content-end"),
                                
                                ]
                                ),
                        dbc.Row(
                            [
                                dbc.Col(id="topSalesItemGraph"),
                            ]
                        ),

                    ], style={

                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        # 'height': '550px',
                        'background-color': 'white',
                        # 'width': '100%',
                        # 'display': 'flex',
                        'justify-content': 'center',
                    }
                ),
            ], className="mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-8"),
        # SECOND COL
        html.Div(dbc.Col([

                html.Div(
                    [
                        dbc.Row([
                            dbc.Col(html.Div(id="topCustsTitle", style={
                                            'font-size':'24px',
                                            'margin-top':'30px',
                                            'margin-left':'50px',
                                            'font-weight':'bold'
                              
                            }), className=" mr-5 d-flex justify-content-start"), 
                            dbc.Col(html.Div(
                                id='custsDropDownDiv',
                                 style={
                                    'justify-content': 'end',
                                    'align-content': 'center',    'text-align': 'center',
                                    'min-width': '100px',
                                    'margin-top': '30px',
                                    'font-size': '13px',
                                },), className=" mr-5 d-flex justify-content-end"),
                            ]
                                ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(id='getSalesCustomerGraph',
                                                 style={
                                                     'margin-top': '5px', }
                                                 )
                                    ], width=12
                                ),
                            ]
                        ),


                    ]
                ),

                ],
                style={

                        'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                        'background-color': 'white',
                        # 'height': '550px',
                        # 'width': '100%',
                        'justify-content': 'center',
                    }), className="mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-4"),
    ]

def selectedMonthyearGraphs():
    mainDict=lastLang[-1]
    return [
        
        #  COL ONE
        html.Div([
            dbc.Row(

                dbc.Col([

                        dbc.Row([
                            dbc.Col(html.Div(id='salesGraphTitle',style={
                                 'font-size': '25px',
                                     'font-weight': 'bold',
                            }),className="mt-3 ml-5 d-flex justify-content-start"),
                            dbc.Col(
                             [
                                 html.Div(id='select-year-title-div', style={
                                     'margin-right': '15px',
                                     'font-size': '18px',
                                    #  'font-weight': 'bold',
                                 }),
                                 html.Div(
                                     id='select-year-div',)], className="mt-3 d-flex justify-content-end",style={'margin-right':-30}
                                     ),

                            dbc.Col(
                                [

                                    html.Div(id='select-month-title-div', style={
                                        'margin-right': '15px',
                                        'font-size': '18px',
                                        # 'font-weight': 'bold',
                                    }),
                                    html.Div(
                                        id='dropdown2Div',)


                                ], className="mt-3  mr-5 d-flex justify-content-end"),

                            ]),

                        dbc.Row([

                            dbc.Col(
                                id="graph", style={
                                    # 'margin-left': '5px',
                                    'margin-bottom': '10px', }),
                        ]),
                   
                ]), style={
                    'margin-left': '1px',
                    'margin-right': '1px',
                    'height':'500px',
                    'background-color': 'white',
                    'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',

                }
            ),
           
            
        
        ], className="mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-7"),
        
        # COL SECOND
        html.Div(
           html.Div(id='pieGraph',  style={
                'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
                'height':'500px',
                'background-color': 'white',

                # 'width': '95%',
                }), className="mt-3 col-sm-12 col-md-12 col-lg-12 col-xl-5")

    ]

def yearMonthPlot(month, year, title):
    # print('INSIDE YEAR MONTH PLOT')
    # MONTH AN YEAR DATA
    data = sales
    
    data = data[data['Year'] == int(year)]
    data = data[data['Month'] == int(month)]
    month_values = weeksEval(data)
    labels = []
    values = []
    for val in month_values:
        label, value = val
        labels.append(label)
        values.append(value)
    # print('EVAL MONTH DONE')
    nowMonth = pd.DataFrame(data.groupby('InvoiceDate').Total.sum())
    mean = nowMonth["Total"].mean()
    nowMonth['Mean'] = mean
    # TOTAL ITEMS
    selectedTotalItems = itemMostYears[yearsName.index(int(year))]
    selectedTotalItems = [g for n, g in selectedTotalItems.groupby(
        pd.Grouper(key='InvoiceDate', freq='M'))]
    selectedTotalItems = selectedTotalItems[int(month)-1]
    selectedTotalItems['ItemNo'] = selectedTotalItems['ItemNo'].astype(int)
    # # MOST ITEM
    selectedMostItem = itemMostYears[yearsName.index(int(year))]
    selectedMostItem = [g for n, g in selectedMostItem.groupby(
        pd.Grouper(key='InvoiceDate', freq='M'))]
    selectedMostItem = selectedMostItem[int(month)-1]
    selectedMostItem['ItemNo'] = selectedMostItem['ItemNo'].astype(int)
    # TOTAL SALES
    totalSale = sum(nowMonth['Total'])
    # print('CALLING RETURNS')
    # TOTAL PROFIT
    profit = sum(data['Total'])-sum(data['TotalCost'])
    # TOP CUSTOMER
    nowCust = data
    nowCust = pd.DataFrame(nowCust.groupby('CustomerNo').Total.sum())
    nowCust = nowCust[nowCust['Total'] == max(nowCust['Total'])]
    cust = nowCust.index[0]
    return (
        selectedMonthGraph(nowMonth, title),
        selectedMonthPie(labels, values),
        selectedMonthTotalSale(totalSale),
        selectedMonthTotalItems(selectedTotalItems),
        selectedMostItemSold(selectedMostItem),
        selectedMostProfit(profit),
        selectedMonthTopCustomer(cust)
    )

def selectedMonthPie(labels, values):
    mainDict=lastLang[-1]
    colors = ['#2D3E36', '#006B5B', '#009D4E', '#25C45F', '#6AC738']
    
    pull=[0,0,0,0,0.1]
    if len(labels) == 6:
        # colors = ['#89BB50', '#70bb50', '#87C453', '#8AC954', '#99ed4a']
        pull=[0,0,0,0,0,0.1]
    if len(labels) == 4:
        # colors = [ '#50B861', '#25C45F', '#62D654', '#3FC470']
        pull=[0,0,0,0.1]
    if len(labels) == 3:
        # colors = ['#25C45F', '#62D654', '#3FC470']
        pull=[0,0,0.1]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                pull=pull,
                marker_colors=colors
            )],
            
    )
    fig.update_layout(
        margin= dict(
                   l= 0,
                   r= 0,
                   b= 0,
                   t= 70,
                   pad= 0
                 ),
      
        title=f'<b>{mainDict["Weeks breakdown"]}</b> '+f'<b>({mainDict[monthNames[selectedMonth[-1]-1]]}, {selectedYear[-1]} )</b>',
        title_font_size=24,
        # autosize=True,
        
        legend=dict(
            orientation="h",
            xanchor="right",
            yanchor="bottom",
        x=0.95,
        y=-0.1,
        font=dict(
            size=18,
            color="black"
        ),)
        
    )
    fig.update_traces(textposition='inside', textfont_size=16)
    return dcc.Graph(figure=fig)

# MAIN DROPDOWN CALLBACK

@app.callback(
    dash.dependencies.Output('topCustsTitle', 'children'),
    dash.dependencies.Output('topItemsTitle', 'children'),
    dash.dependencies.Output('salesGraphTitle', 'children'),
    dash.dependencies.Output('graph', 'children'),
    dash.dependencies.Output('pieGraph', 'children'),
    dash.dependencies.Output('selectedMonthTotalSale', 'children'),
    dash.dependencies.Output('selectedMonthTotalItems', 'children'),
    dash.dependencies.Output('selectedMostItemSold', 'children'),
    dash.dependencies.Output('selectedMonthProfit', 'children'),
    dash.dependencies.Output('selectedMonthTopCustomer', 'children'),
    dash.dependencies.Output('itemsDropDownDiv', 'children'),
    dash.dependencies.Output('custsDropDownDiv', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def selectedMonthYearCallBack(value):
    mainDict=lastLang[-1]
    if value == None:
        selectedMonth.append(6)
    else:
        selectedMonth.append(value)

    topitemsTitle=f"{mainDict['Top Items']} ({mainDict[monthNames[selectedMonth[-1]-1]]}, {selectedYear[-1]})"
    topCustsTitle=f"{mainDict['Top Customers']} ({mainDict[monthNames[selectedMonth[-1]-1]]}, {selectedYear[-1]})"
    title = f"{mainDict['Sales']} ({mainDict[monthNames[selectedMonth[-1]-1]]}, {selectedYear[-1]})"
    (graph,
     pie,
     totalSale,
     selectedMonthTotalItems,
     selectedMostItemSold,
     profit,
     topCust
     ) = yearMonthPlot(selectedMonth[-1], selectedYear[-1], title)

    return (
        topCustsTitle,
        topitemsTitle,
        title,
        graph,
        pie,
        totalSale,
        selectedMonthTotalItems,
        selectedMostItemSold,
        profit,
        topCust,
        dcc.Dropdown(
                                    id='itemsDropDown',
                                    options=[
                                        {'label': f'{mainDict["Top"]} 5', 'value': 5},
                                        {'label': f'{mainDict["Top"]} 10', 'value': 10},
                                        {'label': f'{mainDict["Top"]} 15', 'value': 15},
                                    ],
                                    value=10,
                                    searchable=False,
                                    style={'width': '150px'}
                                ),dcc.Dropdown(
                                    id='custsDropDown',
                                    options=[
                                        {'label': f'{mainDict["Top"]} 5', 'value': 5},
                                        {'label': f'{mainDict["Top"]} 10', 'value': 10},
                                        {'label': f'{mainDict["Top"]} 15', 'value': 15},
                                    ],
                                    value=10,
                                    searchable=False,
                                    style={'width': '150px'}
                                ))


@app.callback(
    dash.dependencies.Output('dropdown2Div', 'children'),
    [dash.dependencies.Input('dropdown1', 'value')])
def dropdown1CallBack(value):
    if value == None:
        selectedYear.append(2020)
    else:
        selectedYear.append(value)
    return dcc.Dropdown(
                        id='dropdown2',
                        options=getMonthsDCC(),
                        searchable=False,
                        value=6,
                        style={'width': '150px'}
                    )
    
 



@app.callback(
    dash.dependencies.Output('topSalesItemGraph', 'children'),
    [dash.dependencies.Input('itemsDropDown', 'value')])
def itemsDropDownCallBack(value):
    mainDict=lastLang[-1]
    if value == None:
        value=10

    print(f'ITEMS TOP VALUE {value}, {selectedMonth[-1]}, {selectedYear[-1]},')
    (top_items,
     top_items_sales,
     top_items_costs,
     top_items_profits) = itemsF.getCostPriceProfit(value, selectedMonth[-1], selectedYear[-1])
    return itemsF.getItemGraph(top_items, top_items_sales,
                            top_items_costs, top_items_profits,mainDict)
    
@app.callback(
    dash.dependencies.Output('getSalesCustomerGraph', 'children'),
    [dash.dependencies.Input('custsDropDown', 'value')])
def custsDropDownCallBack(value):
    mainDict=lastLang[-1]
    if value == None:
        value=10
    return cust.getTopCustomer(value, selectedMonth[-1], selectedYear[-1],mainDict)
    