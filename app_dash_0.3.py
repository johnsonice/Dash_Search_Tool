import base64
import datetime
import io
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from docx import Document
import pandas as pd
import json 
import copy
import time

import os
import sys
sys.path.insert(0,'./dashboard')
from process_util import Processor
from evaluate import get_topic_df
from graph_historical_util import get_county_df,get_top_topic_ids,get_plot_df_list,aggregate_doc_topic_distribution
import config
#%%
## initialize processor
processor = Processor(model_path=None,
                      dictionary_path=None,
                      country_map_path=config.country_map_path,
                      custom_file = config.adhoc_check_file_path)


## get minium requirement 
custom_groups_keys = list(processor.custom_finder.custom_dict_sets.keys())
custom_items_sets = {k:[{'label':hi,'value':hi} for hi in list(processor.custom_finder.custom_dict_sets[k].keys())] 
                        for k in custom_groups_keys}

def build_check_items(custom_items_sets):
    ## hotbutton issues 
    elements = []
    for header,check_items in custom_items_sets.items():
        ele = html.Div(children=[
                    html.H5(header,
                            style={'margin': '5px',
                                   'padding':'5px',
                                   }),
                    dcc.Checklist(
                        id=header,
                        options=check_items,
                        values=[],
                        labelStyle={'display': 'inline-block',
                                    'padding':"10px",
                                    'width':'23.5%',
                                    'borderWidth':'1px',
                                    'margin':'6px',
                                    'borderRadius': '5px',
                                    'borderStyle': 'solid'
                                    }
                    )
                    ],style={'width': '100%','margin': '10px'}
                )
        elements.append(ele)
    
    return elements
#%%
## load dash style
external_stylesheets = [dbc.themes.BOOTSTRAP,'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Loading screen CSS
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/brPBPO.css"})

app.config.requests_pathname_prefix = ''
app.config['suppress_callback_exceptions']=True

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand='SPR Review Document Topic Analysis',
    brand_href="#",
    sticky="top",
)

img_path = './dashboard/src/imf_seal.png'

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

elements = [
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src=encode_image(img_path),
                                 style={'color': '#2c2825','height':'120px'}),
                    ],style={'width':'20%','margin':'10 auto','textAlign': 'center',}),
    
                    html.H3(
                        children='SPR LP Program Document Keywords Match',
                        style={
                            'width':'60%',
                            'textAlign': 'center',
                            'padding-top':'25px',
                            'color':'white'
                        }
                    )
                ],className='row',style={'height':'120px','background-color':'#007bff'}),
            ],style={'margin':'25px 10px 40px 10px','borderRadius': '15px'}),
            
            dcc.Upload(
                    id='upload-data',
                    children=html.Div(id='processing_text',children=[
                        'Drag and Drop or ',
                        html.A('Select Files',style={'color':'blue'})
                        ]),
                    style={
                        'width': '90%',
                        'height': '80px',
                        'lineHeight': '80px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'background-color':'#cccccc',
                        'opacity':'.5',
                        'margin': 'auto auto 20px auto'
                        },
                    # Allow multiple files to be uploaded
                    multiple=True
                )
    ]

elements.extend(build_check_items(custom_items_sets))
elements.extend([    ## store intemediate data
                    html.Div(id='intermediate-value',
                             style={'display': 'none'}),
                    html.Div(id='intermediate-value-2',style={'display': 'none'}),
                ])


app.layout = html.Div(elements,className='container',style={'max-width': '80%'})



#%%

def build_html_table(df,filename,date):
    res = html.Div([
                    html.H5(filename),
                    html.H6(datetime.datetime.fromtimestamp(date)),
            
                    dash_table.DataTable(
                        data=df.to_dict('rows'),
                        columns=[{'name': i, 'id': i} for i in df.columns]
                    ),
            
                    html.Hr(),  # horizontal line

                ])
    return res 

def parse_doc(contents, filename, date,processor=processor):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'docx' in filename.lower():
            # Assume that the user uploaded a docx file
            #res = read_doc(io.BytesIO(decoded))
            doc = processor.read_doc(io.BytesIO(decoded))
            ## get topic df
            topic_df = get_topic_df(processor,doc)
        else:
            return html.Div([
                'You much upload a word document. No other type of document is supported at this point.'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
                        
    #res = html.Div([html.Div("{}".format(i)) for i in res])
    res = build_html_table(topic_df,filename,date)
    return res

def process_input_data(contents, filename, date,processor=processor):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    print(filename,file=sys.stdout)
    try:
        if 'docx' in filename.lower():
            # Assume that the user uploaded a docx file
            #res = read_doc(io.BytesIO(decoded))
            #doc = processor.read_doc(io.BytesIO(decoded))
            ## get country name 
            country_name = processor.country_dector.one_step_get_cname(io.BytesIO(decoded))
            ## get custom keywords check results 
            document_for_keywords_check = processor.custom_finder.read_doc(io.BytesIO(decoded))
            filtered_custom_check = processor.custom_finder.check_all_topics(document_for_keywords_check)
            
            ## get topic df
            #topic_df = get_topic_df(processor,doc)
            
            ## store json data to div
            data_store = {'doc_name':filename,
                          'country_name':country_name,
                          'doc_date':date,
                          #'filtered_hotbutton_issues': filtered_hotbutton_issues,
                          'filtered_custom_check': filtered_custom_check}
                          #'topic_df':topic_df.to_json(orient='split', date_format='iso')}
            return json.dumps(data_store)
            
        else:
#            return html.Div([
#                'You much upload a word document. No other type of document is supported at this point.'
#            ])
            return None
            
    except Exception as e:
        print(e,file=sys.stdout)
        return html.Div([
            'There was an error processing this file.'
        ])

#%%
@app.callback(Output('intermediate-value', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def store_temp_date(list_of_contents, list_of_names, list_of_dates):
    try:
        doc,doc_name,doc_date = list_of_contents[0],list_of_names[0],list_of_dates[0]
        res = process_input_data(doc,doc_name,doc_date)
    except:
        res = None
    
    return res    


def make_item_callback_func(item_id):
    def _function(json_data):
        if json_data is not None and json_data != 'None':
            datasets = json.loads(json_data)
            check_names = datasets['filtered_custom_check'][item_id]
            return check_names
        else:
            return []
    return _function

for k in custom_groups_keys:
    app.callback(Output(k, 'values'),
                  [Input('intermediate-value', 'children')]
                  )(make_item_callback_func(k))

#@app.callback(Output('country-picker', 'style'), 
#              [Input('intermediate-value', 'children')])
#def toggle_container1(data):
#    if data:
#        return {'display': 'block'}
#    else:
#        return {'display': 'none'}

if __name__ == '__main__':
    #app.run_server(port=8888, host='0.0.0.0', debug=True)
    app.run_server(debug=True)