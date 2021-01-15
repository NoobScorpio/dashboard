import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

borderStyle = {

    
    'background-color': 'white',

    'box-shadow': '0px 0px 5px 0px rgba(0,0,0,0.2)',
    'border': '1px solid #ebebeb', }


def getDummyLayout():
    return [
        dbc.Row("NO DATA AVAILABLE",className="d-flex justify-content-center",style={'font-size':'20px','font-weight':'bold'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            dbc.Col([
                                dbc.Row(
                                    [
                                        dbc.Col(['?'], style=borderStyle),
                                        dbc.Col(['?'], style=borderStyle),
                                        dbc.Col(['?'], style=borderStyle),
                                        dbc.Col(['?'], style=borderStyle),
                                        dbc.Col(['?'], style=borderStyle),
                                    ]
                                ),
                            ],
                                width=12)
                        ),

                        dbc.Row(dbc.Col(
                            [
                                    dcc.Graph()
                            ], 
                            style=borderStyle,
                            width=12),className='mt-1'),
                    ],
                    width=8),
                dbc.Col(
                    [
                        dcc.Graph()
                    ],
                    style=borderStyle,
                    width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([ dcc.Graph()],style=borderStyle,width=8),
                dbc.Col([ dcc.Graph()],style=borderStyle,width=4),
            ],className='mt-1'
        ),
    ]
