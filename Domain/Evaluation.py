from Adapters.Data import EvaluationResult
from Adapters.RestServices import list_datasets
from Domain.DictionaryBuilder import retrieve_datasetdictionary
from Adapters.RedisCache import get_datasetlist, set_datasetlist, get_wordscores, set_wordscores, get_datasetdictionary
from Domain.TextDocumentProcessor import preprocess_text, extract_matches


def evaluate(msg: str, user_id: int, is_dialogue: bool) -> dict:
    """Evaluates the mapping scores for each dataset"""
    datasets = get_datasetlist(user_id)
    if datasets is None:
        datasets = list_datasets()
        set_datasetlist(user_id, datasets)

    lemmas = preprocess_text(msg)
    dataset_dictionaries = retrieve_datasetdictionary(datasets.keys(), user_id)

    __update_cache(lemmas, dataset_dictionaries, user_id, is_dialogue)
    results = __find_candidates(user_id, datasets)

    return results


def __update_cache(lemmas: [], dataset_dictionaries: dict, user_id: int, is_dialogue: bool):
    """Updates the cache for wordscores. If its a dialog, scores will be added up per word, otherwise just replaced"""
    for ds_id in dataset_dictionaries.keys():
        wordscores = extract_matches(lemmas, dataset_dictionaries[ds_id])

        if is_dialogue:
            old_scores = get_wordscores(ds_id, user_id)
            if old_scores is not None:
                for score_id in wordscores.keys():
                    old_score = old_scores[score_id]
                    if old_score is not None:
                        wordscores[score_id] = old_score.add_scores(wordscores[score_id], True)

        set_wordscores(ds_id, user_id, wordscores)


def __find_candidates(user_id: int, datasets: dict) -> dict:
    """Calculates the score for a dataset, a length normalized score and collects the mapped words"""

    dataset_results = {}

    for ds_id in datasets.keys():
        wordscores = get_wordscores(ds_id, user_id)
        list_of_words = []
        sum = 0
        for score_id in wordscores.keys():
            score = wordscores[score_id]
            if score is not None:
                sum = sum + score.score
                if score.score != 0:
                    list_of_words.append(wordscores[score_id].word)

        datasetDict = get_datasetdictionary(ds_id, user_id)
        norm_sum = sum/datasetDict.wordcount
        dataset_evaluation = EvaluationResult(ds_id, sum, norm_sum, list_of_words)
        dataset_results[ds_id] = dataset_evaluation

    return dataset_results
