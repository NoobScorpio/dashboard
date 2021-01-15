import dash
import dash_bootstrap_components as dbc
from flask_babel import Babel
FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,FA])
app.config['BABEL_DEFAULT_LOCALE']='en'
babel=Babel(app)