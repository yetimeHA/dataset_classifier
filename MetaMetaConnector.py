import re
import requests

from lexpy.trie import Trie
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer
from spacy.symbols import NOUN
from spacy.lang.en import English

import Config
from Data import DatasetDictionary
from Helpers import get_jwt

nlp = English()
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
tokenizer = nlp.Defaults.create_tokenizer(nlp)


def retrieve_tries(dataset_ids: [], user_id: int) -> dict:
    """Loads lookup tries for a list of datasets"""
    lookup_tries = {}
    for id in dataset_ids:
        lookup_tries[id] = __build_tries(id, user_id)

    return lookup_tries


def __build_tries(dataset_id: int, user_id: int) -> DatasetDictionary:
    """Creates lookup tries from levels and segments"""
    col_unique_values = __get_column_unique_values(dataset_id, user_id)
    all_values = __condense_and_lemmatize(col_unique_values)

    level_trie = Trie()
    level_trie.add_all(all_values)

    colname_trie = Trie()
    colname_trie.add_all(list(col_unique_values.keys()))

    return DatasetDictionary(dataset_id, colname_trie, level_trie)


def __condense_and_lemmatize(col_unique_values: {}) -> list:
    all_values = []

    for segment in col_unique_values:
        for word in col_unique_values[segment]:
            word = re.sub('[^A-Za-z0-9]\d+', '', word)
            if not is_number(word):
                words = tokenizer(word)
                lemmatized = []
                for w in words:
                        lemmatized.extend(lemmatizer(w.text, NOUN))

                if len(lemmatized) == 1:
                    all_values.extend(lemmatized)
                if len(lemmatized) > 1:
                    all_values.append(" ".join(lemmatized))

    return all_values


def __get_column_unique_values(dataset_id, user_id, jwt="") -> dict:
    """Queries MetaMeta Service to retrieve a dictonary of column-unique-values"""
    if jwt == "":
        jwt = get_jwt()
    url = Config.METAMETA_URL + "/dataset/"+str(dataset_id)+"/column-unique-values"
    request_params = {"userId": str(user_id)}
    request_headers = {"x-auth-token": jwt}

    col_uniques_result = requests\
        .get(url, params=request_params, headers=request_headers)\
        .json()

    return col_uniques_result


def is_number(s):
    try:
        complex(s)
    except ValueError:
        return False

    return True
