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
                        labelStyle={'display': 'block'}
                    )
    return ele

def build_card(key,options):
    onecard = dbc.Card(
        [
            #dbc.CardImg(src="/assets/images/placeholder286x180.png", top=True),
            dbc.CardHeader("",style={'background-color':'#a2b9bc'}),
            dbc.CardBody(
                [
                    html.H4(key, className="card-title"),
                    build_filter_check_list(key,options),
                    #dbc.Button("Go somewhere", color="primary"),
                ],
                style={'padding':'1rem'}
            ),
        ],
        style={'width': "14rem",'height':'100%','border':'0'},
    )
    return onecard
##############################################################
    

### build navigation bar ############################
# make a reuseable navitem for the different examples
#nav_item = dbc.NavItem(dbc.NavLink("SPR Review Automation", href="https://www.imf.org"))
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Youtube Channel", href='https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?view_as=subscriber'),
        dbc.DropdownMenuItem("SPR Review Automation", href='https://www.imf.org'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/alpha_vantage_tutorial'),
        dbc.DropdownMenuItem("Plotly / Dash", href='https://dash.plot.ly/'),
        dbc.DropdownMenuItem("Dash Bootstrap", href='https://dash-bootstrap-components.opensource.faculty.ai/'),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)
#Navbar Layout
PLOTLY_LOGO = "https://potluckspaces.sfo2.cdn.digitaloceanspaces.com/static/img/contentcreator.png"
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("SPR Rview Automation", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://www.imf.org",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [#nav_item,
                     dropdown,
                     ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)


#####################################################

filter_tiems_sets = {"Account":[{"label":"PRGT",'value':"PRGT"},{"label":"GRA",'value':"GRA"}],
                     "Stage":[{"label":"Request",'value':"Request"},{"label":"Review",'value':"Review"}],
                     "Document":[{"label":"PN",'value':"PN"},{"label":"SR",'value':"SR"}],
                     "Disbursement":[{"label":"Disbursing",'value':"Disbursing"},{"label":"Emergency",'value':"Emergency"},
                                     {"label":"Precautionary",'value':"Precautionary"},{"label":"Non-Dispursing",'value':"Non-Dispursing"}],
                      }
Fund_color_pallet = [] ## will use color pallet latter

# build cards
cards = cards = dbc.CardDeck([dbc.Col(build_card(k,v),width="auto") for k,v in filter_tiems_sets.items()])

cards = dbc.Row(cards,justify="center")
submit_button = dbc.Row(
                        dbc.Button(id='submit-button', 
                           size="lg",
                           n_clicks=0,
                           children='Submit', 
                           className="mr-1"),
                        justify="center"
                        )   

#%%
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

app.layout = html.Div([
    navbar,
    cards,
    submit_button,
    html.Div(id='number-out')
])



############################################################
# callbacks 
##################################33
# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)


checklist_ids = list(filter_tiems_sets.keys())

@app.callback(
    Output('number-out', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State(i,'value') for i in checklist_ids]
    )
def output(n_clicks, i1,i2,i3,i4):
    if sum([len(i1),len(i2),len(i3),len(i4)])==0:
        return None
    else:
        return html.P('{} {} {} {}'.format(i1,i2,i3,i4))

if __name__ == '__main__':
    app.run_server()
