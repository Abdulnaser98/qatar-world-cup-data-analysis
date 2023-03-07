import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


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
