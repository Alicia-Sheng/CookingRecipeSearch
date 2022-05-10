from typing import Iterator, Dict, Union, Sequence, Generator
from elasticsearch_dsl import Index  # type: ignore
from elasticsearch_dsl.connections import connections  # type: ignore
from elasticsearch.helpers import bulk
from doc_template import BaseDoc


class ESIndex(object):
    def __init__(
        self,
        index_name: str,
        docs: Union[Iterator[Dict], Sequence[Dict]],
    ):
        """
        ES index structure
        :param index_name: the name of your index
        :param docs: wapo docs to be loaded
        """
        # set an elasticsearch connection to your localhost
        connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
        self.index = index_name
        es_index = Index(self.index)  # initialize the index

        # delete existing index that has the same name
        if es_index.exists():
            es_index.delete()

        es_index.document(BaseDoc)  # link document mapping to the index
        es_index.create()  # create the index
        if docs is not None:
            self.load(docs)

    @staticmethod
    def _populate_doc(
        docs: Union[Iterator[Dict], Sequence[Dict]]
    ) -> Generator[BaseDoc, None, None]:
        """
        populate the BaseDoc
        :param docs: wapo docs
        :return:
        """
        for i, doc in enumerate(docs):
            es_doc = BaseDoc(_id=i)
            es_doc.id = doc["id"]
            es_doc.cuisine = doc["cuisine"]
            es_doc.title = doc["title"]
            es_doc.instructions = doc["instructions"]
            es_doc.complexity = doc["complexity"]
            es_doc.fsa_lights_per100g = doc["fsa_lights_per100g"]
            es_doc.healthiness = doc["healthiness"]
            es_doc.ingredients = doc["ingredients"]
            es_doc.ingredients_plain_text = doc["ingredients_plain_text"]
            es_doc.nutr_values_per100g = doc["nutr_values_per100g"]
            es_doc.nutr_values_per100g_energy = doc["nutr_values_per100g_energy"]
            es_doc.nutr_values_per100g_fat = doc["nutr_values_per100g_fat"]
            es_doc.nutr_values_per100g_protein = doc["nutr_values_per100g_protein"]
            es_doc.nutr_values_per100g_salt = doc["nutr_values_per100g_salt"]
            es_doc.nutr_values_per100g_saturates = doc["nutr_values_per100g_saturates"]
            es_doc.nutr_values_per100g_sugars = doc["nutr_values_per100g_sugars"]
            es_doc.url = doc["url"]
            yield es_doc

    def load(self, docs: Union[Iterator[Dict], Sequence[Dict]]):
        # bulk insertion
        bulk(
            connections.get_connection(),
            (
                d.to_dict(
                    include_meta=True, skip_empty=False
                )  # serialize the BaseDoc instance (include meta information and not skip empty documents)
                for d in self._populate_doc(docs)
            ),
        )