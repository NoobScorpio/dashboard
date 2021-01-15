# import db
# data = db.getData()

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app import app
import dash_dangerously_set_inner_html
import pandas as pd

# data=pd.DataFrame([])


# if not data.empty:
#     from sales import salesPageDummy
#     from customers import customersPageDummy
#     from items import itemsPageDummy
#     from suppliers import suppliersPageDummy
# else:
from sales import salesPage
from customers import customersPage
from items import itemsPage
from suppliers import suppliersPage
from employees import employeesPage


boxStyle = {
    'height':  '200px',
    'display': 'flex',
    'width':   '300px',
    'margin': '10px',
    'align-items':  'center',
    'text-align': 'center',
    'justify-content': 'center',
    'background-color': '#f2f2f2',  # rgb(255,25,25)
    'color': '#008080',
    'font-size':  '50px',
    'font-weight': 'bold',
    'border-radius': '10px',

}


def getMainLayout():
    return [
        #
        # Section 1
        #
        html.Section(
            [
                #
                # ROW
                #
                html.Div(
                    [
                      #
                      # CARD 1
                      #
                      html.Div(
                            [
                                
                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-comment-dollar"),
                                                    html.H4("Sales Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-1"
                                    ),
                                    className="card"
                                ),href="/sales/salesPage")

                            ],
                            className="col-1-of-3"
                        ),
                        #
                        # CARD 2
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-users"),
                                                    html.H4("Customer Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-2"
                                    ),
                                    className="card"
                                ),href="/customers/customersPage")

                            ],
                            className="col-1-of-3"
                        ),
                        #
                        # CARD 2
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-box-open"),
                                                    html.H4("Items Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-3"
                                    ),
                                    className="card"
                                ),href="/items/itemsPage")

                            ],
                            className="col-1-of-3"
                        ),

                    ],  # ROW
                    className="row-card"
                ),
            ],
            className="section-plans"
        ),
        #
        # Section 2
        #
        html.Section(
            [
                #
                # ROW
                #
                html.Div(
                    [
                      #
                      #CARD 3
                      #
                        html.Div(
                            [
                              
                               dcc.Link( html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-briefcase"),
                                                    html.H4("Employee Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-4"
                                    ),
                                    className="card"
                            ),href="/employees/employeesPage")
                            ],
                            className="col-1-of-3"
                        ),
                        #
                        # CARD 2
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-truck"),
                                                    html.H4("Supply Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-5"
                                    ),
                                    className="card"
                                ),href="/suppliers/suppliersPage")

                            ],
                            className="col-1-of-3"
                      ),
                        #
                        # CARD 3
                        #
                        html.Div(
                            [

                                dcc.Link(html.Div(

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-city"),
                                                    html.H4("Branches Report",
                                                            className="card__heading")

                                                ],
                                                className="card__title card__title--1"
                                            ),
                                            html.Div(
                                                html.Ul(
                                                    [
                                                        html.Li("General"),
                                                        html.Li(
                                                            "Advanced"),
                                                        html.Li("KPI"),
                                                        html.Li(
                                                            "Prediction"),

                                                    ]
                                                ),
                                                className="card__details"
                                            ),
                                        ],
                                        className="card__side card__side--front-6"
                                    ),
                                    className="card"
                                ),href="/branches/branchesPage")

                            ],
                            className="col-1-of-3"
                        ),

                    ],  # ROW
                    className="row-card"
                ),
            ],
            className="section-plans"
        ),
    ]

# LAYPOUT
app.layout = html.Div([
  dbc.Navbar(
    [
      dbc.Row(
                [
                    dbc.Col(html.I(className="fas fa-chart-bar fa-4x",style={'color':'white'})),
                    dbc.Col(dbc.NavbarBrand("Bi Dashboard", className="ml-1",style={'font-size':'22px','font-weight':'bold'})),
                ],
                align="center",
                no_gutters=True,
            ),
        
    ],
    color="#45d364",
    dark=True,
),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


def dummyLayout():
    return dbc.Row([
        dcc.Link(html.Div('Sales', style=boxStyle),
                 href='/sales/salesPageDummy'),

        dcc.Link(html.Div('Customers', style=boxStyle),
                 href='/customers/customersPageDummy'),

        dcc.Link(html.Div('Items', style=boxStyle),
                 href='/items/itemsPageDummy'),

        dcc.Link(html.Div('Suppliers', style=boxStyle),
                 href='/suppliers/suppliersPageDummy'),

    ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):

    # ORIGINAL LAYOUT
    print(pathname)
    if pathname == '/sales/salesPage':
        return html.Div(salesPage.salesPageLayout())

    if pathname == '/':
        # if not data.empty:
        #     return dummyLayout()
        # else:
        return getMainLayout()

    elif pathname == '/customers/customersPage':
        print('GETTING INSIDE CUSTOMERS PAGE')
        return html.Div(customersPage.customersPageLayout())
    elif pathname == '/items/itemsPage':
        return html.Div(itemsPage.itemsPageLayout())
    elif pathname == '/suppliers/suppliersPage':
        return html.Div(suppliersPage.suppliersPageLayout())
    elif pathname == '/employees/employeesPage':
        return html.Div(employeesPage.employeesPageLayout())

    # DUMMY LAYOUT
    # print(pathname)
    # if pathname == '/sales/salesPageDummy':
    #     return html.Div(salesPageDummy.getDummyLayout())
    # elif pathname == '/customers/customersPageDummy':
    #     print('GETTING INSIDE CUSTOMERS PAGE')
    #     return html.Div(salesPageDummy.getDummyLayout())
    # elif pathname == '/items/itemsPageDummy':
    #     return html.Div(salesPageDummy.getDummyLayout())
    # elif pathname == '/suppliers/suppliersPageDummy':
    #     return html.Div(salesPageDummy.getDummyLayout())
    


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port='5000', debug=False)
# host='0.0.0.0',