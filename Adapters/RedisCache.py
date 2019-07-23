import pickle

import jsons
from enum import Enum

import redis
import Config
from Adapters.Data import DatasetDictionary, WordScore


class CacheOp(Enum):
    DATASET_LIST = "DatasetList"
    DATASET_DICTIONARY = "DatasetDictionary"
    WORDSCORES = "WordScores"


redis_cache = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


def get_datasetlist(user_id: int) -> dict:
    key = __get_cache_key(CacheOp.DATASET_LIST, -1, user_id)
    ds_list = redis_cache.get(key)
    if ds_list is not None:
        return pickle.loads(ds_list)
    else:
        return None


def set_datasetlist(user_id: int, dataset_list: dict) -> dict:
    key = __get_cache_key(CacheOp.DATASET_LIST, -1, user_id)
    redis_cache.set(key, pickle.dumps(dataset_list))


def get_datasetdictionary(dataset_id: int, user_id: int) -> DatasetDictionary:
    key = __get_cache_key(CacheOp.DATASET_DICTIONARY, dataset_id, user_id)
    ds_dict = redis_cache.get(key)
    if ds_dict is not None:
        return pickle.loads(ds_dict)
    else:
        return None


def set_datasetdictionary(dataset_id: int, user_id: int, dictionary: DatasetDictionary):
    key = __get_cache_key(CacheOp.DATASET_DICTIONARY, dataset_id, user_id)
    redis_cache.set(key, pickle.dumps(dictionary))


def get_wordscores(dataset_id, user_id):
    key = __get_cache_key(CacheOp.WORDSCORES, dataset_id, user_id)
    cache_result = redis_cache.get(key)
    if cache_result is not None:
        scores_dict = pickle.loads(cache_result)
        return scores_dict
    else:
        return None


def set_wordscores(dataset_id, user_id, scores):
    key = __get_cache_key(CacheOp.WORDSCORES, dataset_id, user_id)
    redis_cache.set(key, pickle.dumps(scores))


def delete(dataset_id, user_id):
    wordscores_key = __get_cache_key(CacheOp.WORDSCORES, dataset_id, user_id)
    redis_cache.delete(wordscores_key)


def __get_cache_key(cache_op: CacheOp, dataset_id: int, user_id: int) -> str:
    key = cache_op.value+":::"+str(dataset_id)+":::"+str(user_id)
    return key