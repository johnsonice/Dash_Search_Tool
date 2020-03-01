#######
# A very basic Input/Output callback, with State!
######
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import requests, base64
from io import BytesIO
from dash.dependencies import Input, Output, State


##### dash page build functions ######################3
def build_filter_check_list(key,options):
    ## hotbutton issues 
    ele = dcc.Checklist(
                        id=key,
                        options=options,
                        value=[],
                        labelStyle={}
                    )
    return ele



##############################################################
    

### build navigation bar ############################
# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("SPR Review Automation", href="https://www.imf.org"))
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Youtube Channel", href='https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?view_as=subscriber'),
        dbc.DropdownMenuItem("Potluck App", href='https://cryptopotluck.com/'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/alpha_vantage_tutorial'),
        dbc.DropdownMenuItem("Plotly / Dash", href='https://dash.plot.ly/'),
        dbc.DropdownMenuItem("Dash Bootstrap", href='https://dash-bootstrap-components.opensource.faculty.ai/'),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)



#####################################################

filter_tiems_sets = {"content":[{"label":"PRGT",'value':"PRGT"},{"label":"GRA",'value':"GRA"}],
                     "content2":[{"label":"C",'value':"C"},{"label":"D",'value':"D"}]
                                 }
#check_elements = build_filter_check_list(filter_tiems_sets)


cardone = dbc.Card(
    [
        #dbc.CardImg(src="/assets/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                build_filter_check_list('content',filter_tiems_sets['content']),
                #dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)
cardtwo = dbc.Card(
    [
        #dbc.CardImg(src="/assets/images/placeholder286x180.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                #dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

cards = dbc.Row(
    [dbc.Col(cardone, width="auto"), dbc.Col(cardtwo, width="auto")]
)

#%%
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

app.layout = html.Div([
    cards,
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Submit',
        style={'fontSize':28}
    ),
    html.H1(id='number-out')
])



############################################################





@app.callback(
    Output('number-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('content', 'value')]
    )
def output(n_clicks, v1):
    return 'displayed after {} {} {}clicks'.format(n_clicks,v1)

if __name__ == '__main__':
    app.run_server()
