import math
import time

from spacy.lang.en import English, LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer

import Config
from Data import WordScore, DatasetDictionary

nlp = English()
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)


def preprocess_text(text: str) -> list:
    """Creates a list of words from text document with words in their lemma form"""
    document_words = []

    document = nlp(text)
    for word in document:
        if not word.is_stop and not word.is_punct:
            new_word = word.lemma_
            document_words.append(new_word.lower())

    return document_words


def extract_matches(lemmatized_text: [], dataset_tries: DatasetDictionary) -> dict:
    """Extracts matches of a dataset dictionary against a given text considering lemma-form"""
    word_scores = {}

    for word in lemmatized_text:
        current_score: WordScore = word_scores.get(word, WordScore(word, 0, time.time()))
        new_score: WordScore = __score_word(word, dataset_tries)
        current_score.add_scores(new_score)
        word_scores[word] = current_score

    return word_scores


def __score_word(word: str, dataset_tries: DatasetDictionary) -> WordScore:
    """Scores words based on their matches against the dataset vocabulary"""
    highscore = 0

    if word in dataset_tries.colname_trie:
        highscore = 1 * Config.COLUMN_SCORES_WEIGHT
    elif word in dataset_tries.level_trie:
        highscore = 1
    else:
        col_contains = dataset_tries.colname_trie.search("*" + word + "*")
        for match in col_contains:
            score = __get_length_ratio(match, word) * Config.COLUMN_SCORES_WEIGHT
            if highscore < score:
                highscore = score

        level_contains = dataset_tries.level_trie.search("*" + word + "*")
        for match in level_contains:
            score = __get_length_ratio(match, word)
            if highscore < score:
                highscore = score

        leven_dist = __get_levenstein_dist(word)
        col_distance = dataset_tries.colname_trie.search_within_distance(word, dist=leven_dist)
        for match in col_distance:
            score = __get_length_ratio(match, word) / leven_dist * Config.COLUMN_SCORES_WEIGHT
            if highscore < score:
                highscore = score

        level_distance = dataset_tries.level_trie.search_within_distance(word, dist=leven_dist)
        for match in level_distance:
            score = __get_length_ratio(match, word) / leven_dist
            if highscore < score:
                highscore = score

    return WordScore(word, highscore, time.time())


def __get_length_ratio(word1: str, word2: str) -> float:
    if len(word1) > len(word2):
        return len(word1)/len(word2)
    else:
        return len(word2)/len(word1)


def __get_levenstein_dist(word: str) -> int:
    """Determines the allowed maximum levenstein distance for a word and its match, eg LEVENSTEIN_RATIO = 5 means
    1 mismatch allowed for every 5 letters"""
    return math.ceil(len(word) / Config.LEVENSTEIN_RATIO)
