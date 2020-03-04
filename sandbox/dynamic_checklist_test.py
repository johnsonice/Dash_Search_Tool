#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 20:50:32 2020

@author: chengyu
"""
import dash
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


check_options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ]
test_ele = dcc.Checklist(
                id = 'test-id',
                options=[],
                value=['MTL', 'SF']
                )  
lable_ele = html.Label('Dropdown')
button_ele = html.Button('Submit', id='button',n_clicks=0)
p_ele = html.Div(id='output-container-button',
             children='Enter a value and press submit')
elements = [lable_ele,test_ele,button_ele,p_ele]

## build app layout 
app.layout = html.Div(elements, style={'width': '50%'})



##%%
## callbacks 
@app.callback(
            ## for output div, we choose children property, whcih is the default
            Output(component_id='test-id',component_property='options'),
            [Input(component_id='button',component_property='n_clicks')] 
            )
def update_output_div(input_value):
    if input_value==0:
        return []
    else:
        return check_options





if __name__ == '__main__':
    app.run_server(debug=True)
