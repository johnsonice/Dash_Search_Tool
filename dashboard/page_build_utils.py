#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 23:45:58 2020

@author: huang
"""
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


filter_tiems_sets = {}
def build_filter_check_list(filter_tiems_sets):
    ## hotbutton issues 
    elements = []
    for header,check_items in filter_tiems_sets.items():
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

