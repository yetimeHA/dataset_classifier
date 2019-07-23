# Based on GenSim Tutorial, not part of the dataset classifier
from pprint import pprint

import gensim
import glob
import re
import os

import nltk
import spacy
from gensim import corpora, models
from gensim.models import CoherenceModel

os.system("python -m spacy download en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

import pandas as pd
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords
nltk.download('stopwords')
NUM_TOPICS = 7

stop_words = stopwords.words('english')
stop_words.extend(['from', 'public key', 'www', 'http', 'hey', 'com', 'pm', 'lt', 'yep','hi','vs', 'hk', 'html', 'gt', 'hey', 'png', 'jpg', 'csv', 'jkdrv', 'fa', 'fndm','jsx','mdrm', 'een',
                   'st','cc','hq', 'uafk','qt','haha', 'paa','uanajtb', 'udqestm', 'udq','ucrcmguvc','aayge' , 'ljbhmy', 'zstuuak', 'jjwmd', 'dtkuz', 'ububg', 'mpapfdj', 'hrcnl', 'zsepy',
                   'ueht', 'zt','mpapfdj','zsepy' ])

mallet_path = '../mallet-2.0.8/bin/mallet' # update this path


def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values

if __name__ == '__main__':
    general_dataframe = pd.DataFrame()

    for file in glob.glob("/Users/yetime/DatasetIdentifier/Data/Hyper Anna Slack export Aug 9 2016 - Apr 30 2019/anna_engineering/*.json"):

        df = pd.read_json(file)
        general_dataframe=general_dataframe.append(df, sort=False, ignore_index=True)

    text_data = general_dataframe.text.values.tolist()

    # Remove UserIDs
    data = [re.sub('<@[A-Z0-9]*>', '', t) for t in text_data]

    # Remove emojies
    data = [re.sub(':[a-z_\-]*:', '', t) for t in text_data]

    #remove replies to ssh key
    data = [re.sub('<mailto:.*>', '', t) for t in text_data]

    data_words = list(sent_to_words(data))

    print("DATA WORDS: \n")
    print(data_words)

    # Build the bigram and trigram models
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)  # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    data_words_nostops = remove_stopwords(data_words)
    data_words_bigrams = make_bigrams(data_words_nostops)
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    # Create Dictionary
    id2word = corpora.Dictionary(data_lemmatized)

    # Create Corpus
    texts = data_words_nostops

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    #Using Mallet Algo
    ldamallet = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=NUM_TOPICS, id2word=id2word)
    # Build the LSI model
    lsi_model = models.LsiModel(corpus=corpus, num_topics=NUM_TOPICS, id2word=id2word)



    # Show Topics
    pprint(ldamallet.show_topics(formatted=False))

    # Compute Coherence Score
    coherence_model_ldamallet = CoherenceModel(model=ldamallet, texts=data_lemmatized, dictionary=id2word,
                                               coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()
    print('\nCoherence Score: ', coherence_ldamallet)

    print("LSI Model:")

    for idx in range(NUM_TOPICS):
        # Print the first 10 most representative topics
        print("Topic #%s:" % idx, lsi_model.print_topic(idx, 10))

    print("=" * 20)

    #assess best number of topics

    #model_list, coherence_values = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=data_lemmatized, start=2, limit=40, step=6)
    #limit = 40
    #start = 2
    #step = 6
    #x = range(start, limit, step)

    #for model_list, coherance_values in zip(x, coherence_values):
    #    print("Num Topics =", model_list, " has Coherence Value of", round(coherance_values, 4))
