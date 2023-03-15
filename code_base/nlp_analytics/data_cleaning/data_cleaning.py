import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
import datetime


def _removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)


# function to remove the punctuations, apostrophe, special characters using regular expressions
def clean_text(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", " is ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = _removeNonAscii(text)
    text = text.strip()
    return text

def remove_stopwords(text):
    """
    remove stop words that convery little to no information about the actual content like the words: the, of, for etc
    Additionally , other domain-specifc words like world , cup , football , team should be also removed
    """
    filtered_sentence = []
    stop_words = stopwords.words('english')
    specific_words_list = ['char', 'u', 'hindustan', 'doj', 'washington','World','Cup','world','cup',
                           'qatar','Qatar','world','World','cup','Cup','wales','fans','said','fifa','football','it','team']
    stop_words.extend(specific_words_list)
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)


# function for lemmatization
def lemmatize(x):
    lemmatizer = WordNetLemmatizer()
    return' '.join([lemmatizer.lemmatize(word) for word in x])



def extract_relevant_articles_bbc(data):
    """
    Extract only relevant articles from bbc , as we first searched after articles that
    contain the word "qatar" and then filtered out articles about the word cup 2022
    """
    data = data.dropna(subset=['main_content'])
    data.reset_index(drop=True, inplace=True)

    # Define the words that should be kept'
    word1 = 'World Cup'
    word2 = 'World Cup 2022'

    # Filter the DataFrame to keep only the rows where the specified column contains any of the words
    data = data[data['main_content'].str.contains(word1, case=False) | data['main_content'].str.contains(word2, case=False)]

    data.reset_index(drop=True, inplace=True)

    return data

# remove the rows , where the "main_content" column is empty
def remove_empty_rows(data):
    data_after_removing_NAN = data.dropna(subset=['main_content'])
    data_after_removing_NAN.reset_index(drop=True, inplace=True)
    return data_after_removing_NAN

def add_extra_date_columns(data,media_outlet):

    if media_outlet == "aljazerra_data":
        # Convert the "date" column of aljazerra dataframe to datetime format
        data['date'] = pd.to_datetime(data['date'],format="Published On %d %b %Y")
        # Extract the month and year components and combine them
        data['month_year'] = data['date'].dt.strftime('%m-%Y')

        return data

    if media_outlet == "bbc_data":
        # convert the "date" column of the BBC dataframe to datetime fomrat
        # replace NAN values in the "date" column with default value date like "01 January 1900"
        data['date'].fillna('01 January 1900', inplace=True)
        # clean the column , such that formates like this "14 February 2023\n14 February 2023" get converted int "14 February 2023"
        data['date'] = data['date'].str.replace('\n.*','')
        # Check if the year is present in the date string
        data['has_year'] = data['date'].str.contains('\d{4}')
        # Convert the rows without year to datetime object with the current year
        data.loc[~data['has_year'], 'date'] = pd.to_datetime(data.loc[~data['has_year'], 'date'] + ' ' + str(datetime.datetime.now().year), format='%d %B %Y')
        # Convert the rows with year to datetime object
        data.loc[data['has_year'], 'date'] = pd.to_datetime(data.loc[data['has_year'], 'date'], format='%d %B %Y')
        # Drop the 'has_year' column
        data.drop('has_year', axis=1, inplace=True)
        # Extract the month and year components and combine them
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d %H:%M:%S')
        data['month_year'] = data['date'].dt.strftime('%m-%Y')

        return data

    if media_outlet == "guardian":
        # Extract the month and year components and combine them
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data['month_year'] = data['date'].dt.strftime('%m-%Y')

        return data



def main_clean_data(path_to_raw_data_folder, media_outlets ,cleaned_data_files_extensions,path_to_cleaned_data_folder):

    print("start cleaning the data: ")
    for media_outlet, cleaned_media_outlet_file_extension in zip(media_outlets,cleaned_data_files_extensions):

        # read the data
        # if conditions for each media_outlet, because there are special encoding to some of them like "the guardian"
        if media_outlet == "aljazerra_data":
            raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv",sep=',')
        if media_outlet == "bbc_data":
            raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv")
            raw_data = extract_relevant_articles_bbc(raw_data)
        if media_outlet == "guardian":
            raw_data = pd.read_csv(path_to_raw_data_folder + media_outlet + ".csv",sep= ",",encoding='latin1')

        # replace NAN values in the "title" column with empty string
        raw_data['title'] = raw_data['title'].fillna('h')
        #raw_data['main_content'] = raw_data['main_content'].fillna('h')
        raw_data = remove_empty_rows(raw_data)
        # remove non-ascii chars
        raw_data['main_content'] = raw_data['main_content'].apply(clean_text)
        raw_data['title'] = raw_data['title'].apply(clean_text)
        # remove stop words and also domain specific stop words
        raw_data['main_content'] = raw_data['main_content'].apply(remove_stopwords)
        raw_data['title'] = raw_data['title'].apply(remove_stopwords)
        # add extra date columns
        raw_data = add_extra_date_columns(raw_data,media_outlet)
        # save the cleaned version of the cleaned data into a new csv file
        raw_data.to_csv(path_to_cleaned_data_folder + cleaned_media_outlet_file_extension)
        print("finished cleaning the {} data".format(media_outlet))

    print("finished cleaning the data ")








