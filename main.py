import sys
sys.path.append('/Users/abdulnaser/Desktop/DHKatar/code_base/nlp_analytics/sentiment_analysis')
sys.path.append('/Users/abdulnaser/Desktop/DHKatar/code_base/nlp_analytics/data_cleaning')
sys.path.append('/Users/abdulnaser/Desktop/DHKatar/code_base/nlp_analytics/Named Entity recognition')
sys.path.append('/Users/abdulnaser/Desktop/DHKatar/code_base/data_extraction/scrapers')
#sys.path.append('./code_base/nlp_analytics')
#sys.path.append('./code_base/data_extraction/scrapers')
from data_cleaning import *
from sentiment_analysis import *
from aljazerra_world_cup_2022_scraper import *
from bbc_world_cup_2022_scraper import *
from Named_Entity_recognition import *
import nltk
nltk.download('wordnet')



# ============================================ News artilces of "Aljazerra, BBC and the gaurdian" ========================================================
# Extract the articles data from Al jazerra
#aljazerra_web_scraping_main()
#bbc_web_scraping_main()
# ============================================================= Set file Pathes ========================================================
path_to_raw_data_folder = "./code_base/data_extraction/raw_data/"
path_to_cleaned_data_folder = "./code_base/data_extraction/cleaned_data/"
path_to_evaluation_folder = "./code_base/evaluation/"
media_outlets = ["aljazerra_data","bbc_data","guardian"]
cleaned_data_files_extensions = ["aljazerra_cleaned_data.csv","bbc_cleaned_data.csv","guardian_cleaned_data.csv"]
# =========================================================== Data cleaning ======================================================
main_clean_data(path_to_raw_data_folder,media_outlets,cleaned_data_files_extensions,path_to_cleaned_data_folder)
# ========================================================== Sentiment analysis =========================================================
main_sentiment_analysis(media_outlets,cleaned_data_files_extensions,path_to_cleaned_data_folder,path_to_evaluation_folder)
# ========================================================== Named entity recognition =========================================================
main_NER(path_to_cleaned_data_folder,path_to_evaluation_folder)