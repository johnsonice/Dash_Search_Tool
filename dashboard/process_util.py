from gensim import corpora
from gensim.models import LdaModel
import numpy as np
import sys
import os
import gensim
import pickle
import pandas as pd
import datetime
import time
import spacy
from docx import Document
from country_name_util import Country_detector
from keywords_check_util import Hotbutton_finder,Custom_finder
nlp = spacy.load('en')

class Processor(object):
    """
    an hanlp analyzer object for dependency parsing an other related operations 
    """
    def __init__(self,model_path=None,dictionary_path=None,country_map_path=None,
                 custom_file=None,custom_dict_path=None):
        self.model_path = model_path
        self.dictionary_path = dictionary_path
        
        if model_path is None:
            pass
        else:
            self.vocab_dict =  corpora.Dictionary.load(dictionary_path)
            self.model = LdaModel.load(model_path)
            print('LDA model load successfully. ')
        if country_map_path is not None:
            self.country_dector = Country_detector(country_map_path)
            
        self.custom_finder = Custom_finder(custom_file,custom_dict_path)
        

    @staticmethod
    def read_doc(f_path,word_length_filter=50):
        doc=Document(f_path)
        text_list=[p.text for p in doc.paragraphs if len(p.text)>word_length_filter]
        return text_list
    
    def get_topics(self,para):
        bow = self.para2bow(para)
        return self.model[bow]
    
    def para2bow(self,paragraph):
        tokens = nlp(paragraph)
        lemmas = [t.lemma_ for t in tokens]
        bow = self.vocab_dict.doc2bow(lemmas)
        return bow
    
    def get_topics_list(self,doc):
        res = [*map(self.get_topics, doc)]
        return res 
    
    def infer_single_paragraph(self,paragraph):
        '''Load raw paragraph and model, return cleaned paragraph and topic_label with highest probability'''
        #### Process text using Spacy for Tokenization/Lemmentization and loaded dictionary for bag-of-words
        new_bow = self.para2bow(paragraph)
        ## Make inference using gensim_lda model (converted from mallet) and retrieve Top ID
        topic_prob = self.model[new_bow]
        n, prob = zip(*topic_prob)
        top_id = np.array(n)[np.array(prob).argmax()]
        top_prob = np.array(prob)[np.array(prob).argmax()]

        return top_id, top_prob
    
    @staticmethod
    def get_id2name_map(id2name_path):
        '''load id 2 name as a dictionary'''
        #map_df = pd.read_csv(id2name_path)
        map_df = pd.read_excel(id2name_path,'Gensim Topic to LdaViz Topic')
        id2name = dict(zip(map_df['Gensim topic id'],map_df['label']))
        return id2name
        
    def get_history():
        return None
    #%%
if __name__ == "__main__":
    ## global folder path 
    model_path = os.path.join('./model_weights/mallet_as_gensim_weights_50_2019_03_08')
    dictionary_path = './model_weights/dictionary.dict'
    country_map_path = './model_weights/country_map.xlsx'
    custom_keywords_file = './model_weights/keywords_search/custom_keywords_sets.xlsx'
    ## initialize processor, for this case, we just don't give model path, so that we don't load lda model
    processor = Processor(model_path=None,
                          dictionary_path=None,
                          country_map_path=None,
                          custom_file=custom_keywords_file)
    
    ## try one test file
    text_file_path = "./test/Brazil_2013.DOCX"
    doc = processor.read_doc(text_file_path)
    
    ## check keywords search
    doc_for_topic = processor.custom_finder.read_doc(text_file_path)
    print(processor.custom_finder.check_all_topics(doc_for_topic))
    
    ## get country name 
    print(processor.country_dector.one_step_get_cname(text_file_path))
    #%%
    ## if we give lda model path etc, we can run this 
    tid,tprob= processor.infer_single_paragraph(doc[0])
    print(tid,tprob)
    #%% 

    
    #%%

    
    #%%
#    id2name_path = './model_weights/mapping_file_for_mallet_as_gensim_weights_50_2019_02_12.csv'
#    map_df = pd.read_csv(id2name_path)