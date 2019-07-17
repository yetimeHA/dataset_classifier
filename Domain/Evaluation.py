from Adapters.RestServices import list_datasets
from Domain.DictionaryBuilder import retrieve_datasetdictionary
from Adapters.RedisCache import get_datasetlist, set_datasetlist, get_wordscores, set_wordscores
from Domain.TextDocumentProcessor import preprocess_text, extract_matches


def evaluate(msg: str, user_id: int, is_dialogue: bool):
    datasets = get_datasetlist(user_id)
    if datasets is None:
        datasets = list_datasets()
        set_datasetlist(user_id, datasets)

    lemmas = preprocess_text(msg)
    dataset_dictionaries = retrieve_datasetdictionary(datasets.keys(), user_id)

    __update_cache(lemmas, dataset_dictionaries, user_id, is_dialogue)

    return 0


def __update_cache(lemmas: [], dataset_dictionaries: dict, user_id: int, is_dialogue: bool):
    for ds_id in dataset_dictionaries.keys():
        wordscores = extract_matches(lemmas, dataset_dictionaries[ds_id])

        if is_dialogue:
            old_scores = get_wordscores(ds_id, user_id)
            if old_scores is not None:
                for score in wordscores.keys():
                    old_score = old_scores[score]
                    if old_score is not None:
                        wordscores[score] = old_score.add_scores(wordscores[score], True)

        set_wordscores(user_id, ds_id, wordscores)


def __find_candidates(user_id: int, datasets: dict):
    highscore = 0


