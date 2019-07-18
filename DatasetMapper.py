from typing import Any

from rasa.nlu.components import Component
from rasa.nlu.training_data import Message

from Domain.Evaluation import evaluate


class DatasetMapper(Component):
    """A custom RASA component that scores a given text against available datasets"""

    name = "Dataset Mapper"
    provides = ["datasets"]

    language_list = ["en"]

    def __init__(self, component_config=None):
        super(DatasetMapper, self).__init__(component_config)

    def process(self, message: Message, **kwargs: Any):



if __name__ == '__main__':
    user_id = 0

    conversation_example = "We have been talking a lot recently about all the stuff that has an influence on our" \
                           " sales. Especially produce and products related to meat consumption"

    results = evaluate(conversation_example, user_id, True)

    for r in results.keys():
        print(results[r].dataset_id)
        print(results[r].highscore)
        print(results[r].norm_highscore)
        print(results[r].mapped_words)


