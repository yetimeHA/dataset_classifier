from rasa.nlu.components import Component

from Evaluation import evaluate
from Helpers import list_datasets
from MetaMetaConnector import retrieve_datasetdictionary
from RedisCache import get_datasetlist, set_datasetlist
from TextDocumentProcessor import preprocess_text, extract_matches


class DatasetMapper(Component):
    """A custom RASA component that scores a given text against available datasets"""

    name = "Dataset Mapper"
    provides = ["entities"]
    requires = []
    defaults = {
        "max_time": 300,
        "column_scores_weight": 2.0,
        "levenstein_ratio": 5.0,
        "metameta_url": "http://localhost:9090"
    }
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(DatasetMapper, self).__init__(component_config)

    def convert_to_rasa(self, score, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": score,
                  "confidence": confidence,
                  "entity": "dataset_id",
                  "extractor": "dataset_mapper"}

        return entity


if __name__ == '__main__':
    user_id = 0

    conversation_example = "We have been talking a lot recently about all the stuff that has an influence on our" \
                           " sales. Especially produce and products related to meat consumption"

    evaluate(conversation_example, user_id, True)

