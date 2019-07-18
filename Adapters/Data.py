import Config


class WordScore:
    """Wprd scores and time stamps"""

    def __init__(self, word: str, score: float, timestamp: float=0.0):
        self.word = word
        self.score = score
        self.timestamp = timestamp

    @classmethod
    def from_dict(cls, dictionary) -> 'WordScore':
        return cls(dictionary["word"], dictionary["score"], dictionary["timestamp"])

    def add_scores(self, new_word_score, time_deprec=False):
        if time_deprec:
            timediff = new_word_score.timestamp - self.timestamp
            if timediff > Config.MAX_TIME:
                self.score = new_word_score.score
            else:
                depreciation = 1 - timediff/Config.MAX_TIME
                self.score = self.score*depreciation + new_word_score.score
        else:
            self.score = self.score + new_word_score.score
            if self.timestamp < new_word_score.timestamp:
                self.timestamp = new_word_score.timestamp


class DatasetDictionary:
    """Currently composed of two tries, one for column names and one for the values"""

    def __init__(self, dataset_id, colname_trie, level_trie, wordcount):
        self.dataset_id = dataset_id
        self.colname_trie = colname_trie
        self.level_trie = level_trie
        self.wordcount = wordcount

    @classmethod
    def from_dict(cls, dictionary) -> 'DatasetDictionary':
        return cls(dictionary["dataset_id"], dictionary["colname_trie"], dictionary["level_trie"], dictionary["wordcount"])

class EvaluationResult:
    """Representing the scoring results for a dataset"""

    def __init__(self, dataset_id, highscore, norm_highscore, mapped_words):
        self.dataset_id = dataset_id
        self.highscore = highscore
        self.norm_highscore = norm_highscore
        self.mapped_words = mapped_words

