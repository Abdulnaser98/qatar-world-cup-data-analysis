# calculating the polarity of the news articles
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
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
        print("hello")
        print(line)
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



