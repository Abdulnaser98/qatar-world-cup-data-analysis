from empath import Empath
import nltk


def ts_mod( tokens ):
    """
    This function implements the topic signal approach of Empath. Empath uses a trained (Neuronal Networks) word category list with the aim to detect topic signals in tokenized text. It then sorts the topics by value and shortlist it to the 10 highest ranked topics.
    :param tokens:  tokenized list of words f.ex.: ["cheese","fighting","dog","cold","man","war"]
    :return:        dictionary (created by empath) shortlist of the 10 highest ranked topics - key: detected topic / value: calculated value of importance
    """
    lexicon = Empath()
    lexicon = lexicon.analyze( tokens, normalize=True )

    if lexicon == None:
        return

    topics = threshold_filter( lexicon )
    topics_sorted = sort_topics_by_value( topics )
    topics_shortlist = shortlist_topics( topics_sorted )
    return topics_shortlist


def threshold_filter( lexicon ):
    """
    Implements a threshold for empath values and filters all detected topics below the threshold value. Used to filter irrelevant topics.
    :param lexicon:     dictionary created with empath
    :return:            the filtered dictionary lexicon
    """
    threshold = 0.0000000000000001
    lexicon = { k: v for k,v in lexicon.items() if v >= threshold }
    return lexicon


def sort_topics_by_value( lexicon ):
    """
    Sorts the dictionary of topics descending by their value.
    :param lexicon:     filtered dictionary of topics created with empath
    :return:            sorted dictionary of them topics
    """
    lexicon_sorted = { k: v for k, v in sorted( lexicon.items(), key=lambda item: item[1], reverse=True) }
    return lexicon_sorted


def shortlist_topics( lexicon ):
    """
    Creates a shortlist of the 10 most important topics of a dictionary of sorted topics.
    :param lexicon:     sorted dictionary of topics created with empath
    :return:            shortlist dictionary of the 10 most important topics
    """
    lexicon_shortlist = dict( list( lexicon.items() )[:10] )
    return lexicon_shortlist