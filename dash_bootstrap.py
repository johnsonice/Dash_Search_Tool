#######
# A very basic Input/Output callback, with State!
######
import sys
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import requests, base64
from io import BytesIO
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
sys.path.insert(0,'./dashboard')
#from data_input_utils import filter_tiems_sets,Check_tiems_sets ## input contents for check lists
from data_input_utils import Input_data_processor
from page_build_utils import build_check_items2,build_card


##############################################################
## global variable set up 
check_input_file = './data/ChecklistStata.xlsx'
data_processor = Input_data_processor()
filter_tiems_sets = data_processor.filter_tiems_sets
ids = data_processor.get_custom_sheetnames(check_input_file)
#content_dict,table_dict,draft_req_dict = data_processor.get_dict_by_sheet(check_input_file,ids[0])
Check_tiems_sets = data_processor.get_checklist_items(check_input_file,ids[0])
##############################################################



### build navigation bar ############################
# make a reuseable navitem for the different examples
#nav_item = dbc.NavItem(dbc.NavLink("SPR Review Automation", href="https://www.imf.org"))
dropdown = dbc.DropdownMenu(
    children=[
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
img_path = './dashboard/src/imf_seal.png'
def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        #dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(html.Img(src=encode_image(img_path), height="60px")),
                        dbc.Col(dbc.NavbarBrand("SPR Rview Automation", className='ml-2')),
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
submit_button2 = dbc.Row(
                        dbc.Button(id='submit-button2', 
                           size="lg",
                           n_clicks=0,
                           children='Check', 
                           className="mr-1"),
                        justify="center"
                        )   

file_upload_element = dbc.Row(
                        dbc.Col(
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div(id='processing_text',children=[
                                    'Drag and Drop or ',
                                    html.A('Select Files',style={'color':'blue'})
                                    ]),
                                style={
                                    'width': '60%',
                                    'height': '80px',
                                    'lineHeight': '80px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'background-color':'#cccccc',
                                    'opacity':'.5',
                                    'margin': 'auto auto auto auto'
                                    },
                                # Allow multiple files to be uploaded
                                multiple=True
                                )
                            ),
                        justify='center' ,style={'margin':'1rem','display':'none'},id='upload-data-container'
                        )

#%%
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

app.layout = html.Div([
    navbar,
    cards,
    submit_button,
    file_upload_element,
    build_check_items2(Check_tiems_sets),
    #html.Div(id='check_items',style={'display': 'block'}),
    #submit_button2,
    html.Div(id='intermediate-value',style={'display': 'block'}),
    html.Div(id='intermediate-value-2',style={'display': 'none'}),
])


#%%
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


### prepare variables for callbacks ####
filter_ids = list(filter_tiems_sets.keys())
check_list_ids = list(Check_tiems_sets.keys())
dynamic_checklist_outputs = [Output(c,'options') for c in check_list_ids]
stype_outputs = [Output('checklist1', 'style'),Output('upload-data-container', 'style')]
custom_outputs=stype_outputs + dynamic_checklist_outputs
#dynamic_checklist_options = [Check_tiems_sets[c] for c in check_list_ids] #list(Check_tiems_sets.values())

@app.callback(
    custom_outputs,
    [Input('submit-button', 'n_clicks')],
    [State(i,'value') for i in filter_ids]
    )
def output(n_clicks, i1,i2,i3,i4):
    if sum([len(i1),len(i2),len(i3),len(i4)])==0:
        raise PreventUpdate
    else:
        c_id = "{}_{}_{}_{}".format(i1[0],i2[0],i3[0],i4[0])
        print(c_id)
        res = [{'display':'block'},{'margin':'1rem','display':'block'}]
        #dynamic_checklist_options = [[],[],[]]
        sheet_id = [i for i in ids if c_id in i]
        Check_tiems_sets = data_processor.get_checklist_items(check_input_file,sheet_id[0])
        check_list_ids = list(Check_tiems_sets.keys())
        dynamic_checklist_options = [Check_tiems_sets[c] for c in check_list_ids]
        res.extend(dynamic_checklist_options)
        return res


# @app.callback(
#     Output('intermediate-value', 'children'),
#     [Input('submit-button2', 'n_clicks')],
#     [State('Table','value')]
#     #[State(i,'value') for i in checklist_ids]
#     )
# def output(n_clicks, v):
#     return v
#%%
if __name__ == '__main__':
    app.run_server()
