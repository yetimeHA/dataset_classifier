class WordScore:
    """Wprd scores and time stamps"""

    def __init__(self, word: str, score: float, timestamp: float=0.0):
        self.word = word
        self.score = score
        self.timestamp = timestamp

    def add_scores(self, new_word_score, time_deprec=False):
        if time_deprec:
            timediff = new_word_score.timestamp - self.timestamp
            if timediff > WordScore.MAX_TIME:
                self.score = new_word_score.score
            else:
                depreciation = 1 - timediff/WordScore.MAX_TIME
                self.score = self.score*depreciation + new_word_score.score
        else:
            self.score = self.score + new_word_score.score
            if self.timestamp < new_word_score.timestamp:
                self.timestamp = new_word_score.timestamp


class DatasetDictionary:
    """Currently composed of two tries, one for column names and one for the values"""

    def __init__(self, dataset_id, colname_trie, level_trie):
        self.dataset_id = dataset_id
        self.colname_trie = colname_trie
        self.level_trie = level_trie
