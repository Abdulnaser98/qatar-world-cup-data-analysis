# calculating the polarity of the news articles
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
import math
import pandas as pd
nltk.download('vader_lexicon')
sia = SIA()



def generate_sentiment_scores(data):
    titles = []
    dates = []
    main_contents = []
    title_positive_scores = []
    title_negative_scores = []
    title_neutral_scores = []
    main_content_positive_scores = []
    main_content_negative_scores = []
    main_content_neutral_scores = []
    negatives_mean = []
    positives_mean = []
    neutral_mean = []

    for line,date,title in zip(data['main_content'], data['date'], data['title']):
        titles.append(title)
        dates.append(date)
        main_contents.append(line)



        title_analysed = sia.polarity_scores(title)
        main_content_analysed = sia.polarity_scores(line)

        title_positive_scores.append(title_analysed['pos'])
        title_negative_scores.append(title_analysed['neg'])
        title_neutral_scores.append(title_analysed['neu'])

        main_content_positive_scores.append(main_content_analysed['pos'])
        main_content_negative_scores.append(main_content_analysed['neg'])
        main_content_neutral_scores.append(main_content_analysed['neu'])



        positives_mean.append(( (title_analysed['pos']) + (main_content_analysed['pos']))/2)
        negatives_mean.append( ((main_content_analysed['neg']) + (main_content_analysed['neg']))/2)
        neutral_mean.append( ((main_content_analysed['neu']) + (main_content_analysed['neu']))/2)

    data['title_positive_scores'] = title_positive_scores
    data['title_negative_scores'] = title_negative_scores
    data['title_neutral_scores'] = title_neutral_scores
    data['main_content_positive_scores'] = main_content_positive_scores
    data['main_content_negative_scores'] = main_content_negative_scores
    data['main_content_neutral_scores'] = main_content_neutral_scores
    data['title_main_content_positive_mean'] = positives_mean
    data['title_main_content_negaitve_mean'] = negatives_mean
    data['title_main_content_neutral_mean'] = neutral_mean

    return data



def generate_general_statistical_sentiment_scores(data):
    sentiment_scores_general = {'positive_mean':data['title_main_content_positive_mean'].mean(), 'negatives_mean':data['title_main_content_negaitve_mean'].mean(), 'neutral_mean': data['title_main_content_neutral_mean'].mean()}
    return sentiment_scores_general


def generate_title_statistical_sentiment_scores(data):
    sentiment_scores_titles = {'positive_mean': data['title_positive_scores'].mean(), 'negatives_mean': data['title_negative_scores'].mean(), 'neutral_mean':data['title_neutral_scores'].mean()}
    return sentiment_scores_titles


def main_sentiment_analysis(media_outlets,cleaned_data_pathes,path_to_cleaned_data_folder,path_to_evaluation_folder):

    print("generating sentiment scores: ")
    media_outlets_names = []
    article_positive_means = []
    article_negative_means = []
    title_positive_means = []
    title_negative_means = []
    for media_outlet,cleaned_media_outlet_path in zip(media_outlets,cleaned_data_pathes):
        data = pd.read_csv(path_to_cleaned_data_folder+cleaned_media_outlet_path)
        sentiment_scores = generate_sentiment_scores(data)
        general_statistical_sentiment_scores = generate_general_statistical_sentiment_scores(sentiment_scores)
        title_statistical_sentiment_scores = generate_title_statistical_sentiment_scores(sentiment_scores)
        media_outlets_names.append(media_outlet)
        article_positive_means.append(general_statistical_sentiment_scores.get("positive_mean"))
        article_negative_means.append(general_statistical_sentiment_scores.get("negatives_mean"))
        title_positive_means.append(title_statistical_sentiment_scores.get("positive_mean"))
        title_negative_means.append(title_statistical_sentiment_scores.get("negatives_mean"))
        sentiment_scores.to_csv(path_to_cleaned_data_folder+cleaned_media_outlet_path)
        print("finshed generating sentiment scores for the media outlet {}".format(media_outlet))

    sentiment_analysis_statistcs = pd.DataFrame({'media_outlet': media_outlets_names, 'article_positive_mean': article_positive_means,
    'article_negative_means':article_negative_means,'title_positive_means':title_positive_means,'title_negative_means':title_negative_means})

    sentiment_analysis_statistcs.to_csv(path_to_evaluation_folder+"sentiment_analysis_statistcs.csv")

    print("finished generating sentiment scores")




















