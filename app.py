import ast
from flask import Flask, render_template, request
from typing import List, Dict, Tuple
from typing import List
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections

app = Flask(__name__)
index_name= "cooking_recipe"
top_k = 20
ONE_PAGE = 8 # maximum number of snippets on one page
response = []
docs = {}

# home page
@app.route("/")
def home():
    """
    home page
    :return: template of home.html
    """
    return render_template("home.html")


# result page
@app.route("/results", methods=["POST"])
def results():
    global response
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["main_query"]

    # Need to take a look at the fat variabel
    # fat = request.form["fat"]  #This line is not working
    ## we can add options of sorting methods here
    q_title = Match(title={"query": query_text})
    # q_instructions = Match(instructions={"query": "Layer"})

    # ===== different sorting options
    # ===== now this is sorted by the length of instructions
    # response = search_by_healthiness(index_name, q_title, top_k)
    response = search_by_instruction_length(index_name, q_title, top_k)
    temp_result = response[:ONE_PAGE]
    return render_template("results_test.html", query=query_text, doc=temp_result)
    # return render_template("results.html", query=query_text, fat=fat, doc=temp_result)

def search(index: str, query: Query, top_k) -> None:
    s = Search(using="default", index=index).query(query)[:top_k]  # initialize a query and return top five results
    r = s.execute()
    return r

def search_by_healthiness(index: str, query: Query, top_k) -> None:
    s = Search(using="default", index=index).query(query)[:top_k].sort({"healthiness": {"order": "desc"}})  # initialize a query and return top five results
    r = s.execute()
    return r
    # for hit in r:
    #     print(
    #         hit.meta.id, hit.meta.score, hit.title, hit.ingredients, hit.healthiness, sep="\t"
    #     )  # print the document id that is assigned by ES index, score and title

def search_by_instruction_length(index: str, query: Query, top_k) -> None:
    s = Search(using="default", index=index).query(query)[:top_k].sort({"instructions_length": {"order": "asc"}})  # initialize a query and return top five results
    r = s.execute()
    return r

if __name__ == "__main__":
    app.run(debug=True, port=5000)
