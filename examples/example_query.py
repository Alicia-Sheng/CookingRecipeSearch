from typing import List

from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Query
from elasticsearch_dsl.connections import connections
#from embedding_service.client import EmbeddingClient

# encoder = EmbeddingClient(host="localhost", embedding_type="sbert")
# encoder = EmbeddingClient(host="localhost", embedding_type="fasttext")

def generate_script_score_query(query_vector: List[float], vector_name: str) -> Query:
    """
    generate an ES query that match all documents based on the cosine similarity
    :param query_vector: query embedding from the encoder
    :param vector_name: embedding type, should match the field name defined in BaseDoc ("ft_vector" or "sbert_vector")
    :return: an query object
    """
    q_script = ScriptScore(
        # query={"match_all": {}},  # use a match-all query
        query={"match_all": {}},  # use a match-all query
        script={  # script your scoring function
            "source": f"cosineSimilarity(params.query_vector, '{vector_name}') + 1.0",
            # "source": f"_score",
            # add 1.0 to avoid negative score
            "params": {"query_vector": query_vector},
        },
    )
    return q_script

def rescore_search(index: str, query: Query, rescore_query: Query) -> None:
    s = Search(using="default", index=index).query(query)[
        :5
    ]  # initialize a query and return top five results
    s = s.extra(
        rescore={
            "window_size": 5,
            "query": {
                "rescore_query": rescore_query,
                "query_weight": 0,
                "rescore_query_weight": 1,
            },
        }
    )
    response = s.execute()
    for hit in response:
        print(
            hit.meta.id, hit.meta.score, hit.title, sep="\t"
        )  # print the document id that is assigned by ES index, score and title

def search(index: str, query: Query) -> None:
    s = Search(using="default", index=index).query(query)[:5].sort({"healthiness": {"order": "desc"}})  # initialize a query and return top five results
    response = s.execute()
    for hit in response:
        print(
            hit.meta.id, hit.meta.score, hit.title, hit.nutr_values_per100g_energy,
            hit.nutr_values_per100g_fat, hit.nutr_values_per100g_protein,
            hit.nutr_values_per100g_salt, hit.nutr_values_per100g_saturates,
            hit.nutr_values_per100g_sugars, hit.URL, sep="\t"
        )  # print the document id that is assigned by ES index, score and title

if __name__ == "__main__":
    # python load_es_index.py --index_name recipe_data --path data/recipes_with_nutritional_info.json
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")

    q_match_all = MatchAll()  # a query that matches all documents
    q_title = Match(
        title={"query": "chicken"}
    )  # a query that matches "D.C" in the title field of the index, using BM25 as default

    q_ingredients = Match(
        ingredients_plain_text={"query": "rice"}
    )

    search(
        "cooking_recipe", q_title
    )  # search, change the query object to see different results

    print("="*20)

    search(
        "cooking_recipe", q_ingredients
    )  # search, change the query object to see different results