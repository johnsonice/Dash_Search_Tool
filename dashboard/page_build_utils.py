#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 23:45:58 2020

@author: huang
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


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
                        value=[],
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

def build_check_items2(custom_items_sets):
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
                        value=[],
                        labelStyle={'display': 'inline-block',
                                    'padding':"10px",
                                    'width':'23.5%',
                                    'borderWidth':'1px',
                                    'margin':'6px',
                                    'borderRadius': '5px',
                                    'borderStyle': 'solid'
                                    }
                    )
                    ],style={'width': '70rem','margin': '10px'}
                )
        ele = dbc.Row(ele,justify="center")
        elements.append(ele)
    
    return dbc.Col(id='checklist1',children=elements,style={'display': 'none'})

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
    """"buid  Cards for checklists"""
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