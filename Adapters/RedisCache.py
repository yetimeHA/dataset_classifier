import jsons
from enum import Enum

import redis
import Config
from Adapters.Data import DatasetDictionary

class CacheOp(Enum):
    DATASET_LIST = "DatasetList"
    DATASET_DICTIONARY = "DatasetDictionary"
    WORDSCORES = "WordScores"


redis_cache = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


def get_datasetlist(user_id: int) -> dict:
    key = __get_cache_key(CacheOp.DATASET_LIST, -1, user_id)
    ds_list = redis_cache.get(key)
    if ds_list is not None:
        return jsons.loads(ds_list)
    else:
        return None


def set_datasetlist(user_id: int, dataset_list: dict) -> dict:
    key = __get_cache_key(CacheOp.DATASET_LIST, -1, user_id)
    redis_cache.set(key, jsons.dumps(dataset_list))


def get_datasetdictionary(dataset_id: int, user_id: int) -> DatasetDictionary:
    key = __get_cache_key(CacheOp.DATASET_DICTIONARY, dataset_id, user_id)
    ds_dict = redis_cache.get(key)
    if ds_dict is not None:
        return jsons.loads(ds_dict)
    else:
        return None


def set_datasetdictionary(dataset_id: int, user_id: int, dictionary: DatasetDictionary):
    key = __get_cache_key(CacheOp.DATASET_DICTIONARY, dataset_id, user_id)
    redis_cache.set(key, jsons.dumps(dictionary))


def get_wordscores(dataset_id, user_id):
    key = __get_cache_key(CacheOp.WORDSCORES, dataset_id, user_id)
    scores = redis_cache.get(key)
    if scores is not None:
        return jsons.loads(scores)
    else:
        return None


def set_wordscores(dataset_id, user_id, scores):
    key = __get_cache_key(CacheOp.WORDSCORES, dataset_id, user_id)
    redis_cache.set(key, jsons.dumps(scores))


def __get_cache_key(cache_op: CacheOp, dataset_id: int, user_id: int) -> str:
    return cache_op.value+":::"+str(dataset_id)+":::"+str(user_id)