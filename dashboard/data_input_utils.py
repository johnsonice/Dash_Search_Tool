#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 21:48:43 2020

@author: chengyu
"""

import os,sys
import pandas as pd
import re
filter_tiems_sets = {"Account":[{"label":"PRGT",'value':"PRGT"},{"label":"GRA",'value':"GRA"}],
                     "Stage":[{"label":"Request",'value':"Request"},{"label":"Review",'value':"Review"}],
                     "Document":[{"label":"PN",'value':"PN"},{"label":"SR",'value':"SR"}],
                     "Disbursement":[{"label":"Disbursing",'value':"Disbursing"},{"label":"Emergency",'value':"Emergency"},
                                     {"label":"Precautionary",'value':"Precautionary"},{"label":"Non-Dispursing",'value':"Non-Dispursing"}],
                      }

class Input_data_processor(object):
    def __init__(self,input_file_path=None):
        self.filter_tiems_sets = filter_tiems_sets ## read_filter_items()
        #self.ids = self.get_custom_sheetnames(input_file_path)
        
    @staticmethod
    def read_filter_items(input_file_path):
        """"read filter items from input data"""
        return None
    
    @staticmethod
    def read_check_mappings(input_file_path):
        """"read check items from input data"""
        return None
    
    
    @staticmethod
    def get_sheetnames(input_file_path):
        """"get general sheet names"""
        if input_file_path is None:
            return None
        else:
            excel_file = pd.ExcelFile(check_list_path)
            return excel_file.sheet_names
        
    @staticmethod
    def get_custom_sheetnames(input_file_path):
        if input_file_path is None:
            return None
        else:
            excel_file = pd.ExcelFile(check_list_path)
            check_regex = re.compile(r'^\d+_.*_')
            ids = [s for s in excel_file.sheet_names if check_regex.search(s) is not None]
            return ids
        
        
    @staticmethod
    def get_dict_by_sheet(input_file_path,sheet_name):
        """"read excel file and process content/table/formal drafting requirement"""
        df = pd.read_excel(input_file_path,sheet_name=sheet_name)
        df = df[['Content','key word']].dropna()
        
        ## clear keywords
        def _split(s,sep_pattern=',|;'):
            res = re.split(sep_pattern,s)
            res = [r.strip() for r in res]
            return res
        df['Content'] = df['Content'].apply(lambda x: x.strip())
        df['key word'] = df['key word'] .apply(_split)
        df.set_index('Content',inplace=True)
        
        table_pos = df.index.get_loc('Tables')
        draft_req_pos = df.index.get_loc('Formal Drafting Requirements')
        
        content_df = df[:table_pos]
        table_df = df[table_pos+1:draft_req_pos]
        draft_req_df = df[draft_req_pos+1:]
        
        ## turn to dict
        content_dict = content_df.to_dict()['key word']
        table_dict = table_df.to_dict()['key word']
        draft_req_dict = draft_req_df.to_dict()['key word']
        
        return content_dict,table_dict,draft_req_dict

    def get_checklist_items(self,input_file_path,sheet_name):
        """use checklist input to generate checklist item for page"""
        content_dict,table_dict,draft_req_dict = self.get_dict_by_sheet(input_file_path,sheet_name)
        
        res = {
                "Content":[{'label':k,'value':k} for k in content_dict.keys()],
               "Table":[{'label':k,'value':k} for k in table_dict.keys()],
               "Formal Drafting Requirements":[{'label':k,'value':k} for k in draft_req_dict.keys()],
               }
        
        return res
        
        
#%%

if __name__ == "__main__":
    ## global folder path 
    check_list_path = os.path.join('../data/ChecklistStata.xlsx')
    processor = Input_data_processor(check_list_path)
    ids = processor.get_custom_sheetnames(check_list_path)
    content_dict,table_dict,draft_req_dict = processor.get_dict_by_sheet(check_list_path,ids[0])
    
    for idss in ids:
        Check_tiems_sets1 = processor.get_checklist_items(check_list_path,idss)
        print(Check_tiems_sets1)


#%%
# Check_tiems_sets = {"Content":[
#                                 {"label":"PRGT",'value':"PRGT"},
#                                 {"label":"Type of arrangment",'value':"Type of arrangment"},
#                                 {"label":"Length of arrangment",'value':"Length of arrangment"},
#                                 {"label":"Exceptional access",'value':"Exceptional access"},
#                                 ],
#                     "Table":[
#                                 {"label":"Selected Economic and Financial Indicator",'value':"Selected Economic and Financial Indicator"},
#                                 {"label":"Central/General Government Operations",'value':"Central/General Government Operations"},
#                                 {"label":"Balance of payments ",'value':"Balance of payments"},
#                                 ],
#                     "Formal Drafting Requirements":[
#                                 {"label":"Cover memo",'value':"Cover memo"},
#                                 {"label":"Executive summary",'value':"Executive summary"},
#                                 {"label":"Program modality",'value':"Program modality"},
#                                 ],
#                      }


