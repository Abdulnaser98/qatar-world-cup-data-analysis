import argparse
import sys
sys.path.append('./code_base/nlp_analytics')
from data_cleaning import *
import nltk
nltk.download('wordnet')

import pandas as pd

# clean aljazerra data
aljazerra_raw_data = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/aljazerra_data.csv",sep=';')
# remove the rows , where the "main_content" column was empty
aljazerra_raw_data = remove_empty_rows(aljazerra_raw_data)
# remove non-ascii chars
aljazerra_raw_data['main_content'] = aljazerra_raw_data['main_content'].apply(clean_text)
# remove stop words and also domain specific stop words
aljazerra_raw_data['main_content'] = aljazerra_raw_data['main_content'].apply(remove_stopwords)
# save the cleaned version of the aljazerra data into a new csv file
aljazerra_raw_data.to_csv("./code_base/data_extraction/cleaned_data/aljazerra_cleaned_data.csv")




# clean bbc data
bbc_raw_data = pd.read_csv("/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/all_bbc_qatar_data.csv")
# remove the rows , where the "main_content" column was empty
bbc_raw_data = remove_empty_rows(bbc_raw_data)
# remove non-ascii chars
bbc_raw_data['main_content'] = bbc_raw_data['main_content'].apply(clean_text)
# remove stop words and also domain specific stop words
bbc_raw_data['main_content'] = bbc_raw_data['main_content'].apply(remove_stopwords)
# save the cleaned version of the aljazerra data into a new csv file
bbc_raw_data.to_csv("./code_base/data_extraction/cleaned_data/bbc_cleaned_data.csv")

