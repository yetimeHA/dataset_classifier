import re

from lexpy.trie import Trie
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
from spacy.lemmatizer import Lemmatizer
from spacy.symbols import NOUN
from spacy.lang.en import English

from Adapters.Data import DatasetDictionary
from Adapters.RestServices import get_column_unique_values
from Adapters.RedisCache import get_datasetdictionary

nlp = English()
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
tokenizer = nlp.Defaults.create_tokenizer(nlp)


def retrieve_datasetdictionary(dataset_ids: [], user_id: int) -> dict:
    """Loads lookup tries for a list of datasets"""
    lookup_tries = {}
    for id in dataset_ids:
        tries = get_datasetdictionary(id, user_id)
        if tries is None:
            tries = __build_tries(id, user_id)
        lookup_tries[id] = tries

    return lookup_tries


def __build_tries(dataset_id: int, user_id: int) -> DatasetDictionary:
    """Creates lookup tries from levels and segments"""
    col_unique_values = get_column_unique_values(dataset_id, user_id)
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


def is_number(s):
    try:
        complex(s)
    except ValueError:
        return False

    return True
