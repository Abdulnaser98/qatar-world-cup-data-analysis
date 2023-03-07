import argparse
import sys
sys.path.append('./code_base/nlp_analytics')
from data_cleaning import *
from sentiment_analysis import *
import nltk
nltk.download('wordnet')
import pandas as pd
import numpy as np



# ============================================================= Set Pathes ========================================================
path_to_raw_data_folder = "/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/raw_data/"
path_to_cleaned_data_folder = "./code_base/data_extraction/cleaned_data/"
media_outlets = ["aljazerra_data","all_bbc_qatar_data","guardian"]
cleaned_data_pathes = ["aljazerra_cleaned_data.csv","bbc_cleaned_data.csv","guardian_cleaned_data.csv"]
# =========================================================== Data cleaning ======================================================
print("Cleaning the data: ")
for media_outlet, cleaned_media_outlet_path in zip(media_outlets,cleaned_data_pathes):
    # read the data
    # check if the media outlet is guardian, because there is a special encoding to it
    if media_outlet == "aljazerra_data":
        raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv",sep=';')
    if media_outlet == "all_bbc_qatar_data":
        raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv")
        raw_data = extract_relevant_articles_bbc(raw_data)
    if media_outlet == "guardian":
        raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv",sep= ",",encoding='latin1')
    # reset index and assign it as ID
    raw_data['ID'] = raw_data.reset_index().index
    # remove the rows , where the "main_content" column was empty
    raw_data = raw_data.dropna(subset=['main_content'])
    raw_data.reset_index(drop=True, inplace=True)
    # replace NAN values in the "title" column with empty string
    raw_data['title'] = raw_data['title'].fillna('')
    print("value")
    print(raw_data["main_content"].isnull().sum())
    raw_data = remove_empty_rows(raw_data)
    # remove non-ascii chars
    raw_data['main_content'] = raw_data['main_content'].apply(clean_text)
    raw_data['title'] = raw_data['title'].apply(clean_text)
    # remove stop words and also domain specific stop words
    raw_data['main_content'] = raw_data['main_content'].apply(remove_stopwords)
    raw_data['title'] = raw_data['title'].apply(remove_stopwords)
    # save the cleaned veraion of the cleaned data into a new csv file
    raw_data.to_csv(path_to_cleaned_data_folder + cleaned_media_outlet_path)
    print("finished cleaning the {} data".format(media_outlet))

print("finished cleaning the data ")
# ========================================================== Sentiment analysis =========================================================
"""
print("generating sentiment scores: ")
for filename in cleaned_data_pathes:
    print(filename)
    data = pd.read_csv(path_to_cleaned_data_folder+filename)
    sentiment_scores = generate_sentiment_scores(data)
    sentiment_scores.to_csv(path_to_cleaned_data_folder+filename)
print("finished generating sentiment scores")
"""




















