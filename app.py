import ast
from flask import Flask, render_template, request
from typing import List, Dict, Tuple
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections

# from curses import termattrs
# from operator import methodcaller
# from socket import timeout
# from unittest import result
# from torch import topk
# import json
# from torch import HOIST_CONV_PACKED_PARAMS

app = Flask(__name__)
index_name = "cooking_recipe"
top_k = 20
ONE_PAGE = 8  # maximum number of snippets on one page
response = []
docs = {}
nutrition_options = {"energy": "nutr_values_per100g_energy",
                     "fat": "nutr_values_per100g_fat",
                     "protein": "nutr_values_per100g_protein",
                     "salt": "nutr_values_per100g_salt",
                     "saturates": "nutr_values_per100g_saturates",
                     "sugars": "nutr_values_per100g_sugars"}
cuisine = ''
sort = ''
order = ''

# ************************************************
# general search pages;
# ************************************************
@app.route("/")
def home():
    """
    home page
    :return: template of home.html
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    global response
    global nutrition_options
    global cuisine
    global sort
    global order

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query_text"]
    sort = request.form["sort"]  # sort (complexity, healthiness, fat, ...)
    cuisine = request.form["cuisine"]  # cuisine (all, chinese, ...)
    order = request.form["order"]  # order (desc, asc)

    query = Match(title={"query": query_text})
    response = default_search(index_name, query, top_k, cuisine, sort, order)

    page_id = 1  # set page id to be 1
    result_id = [r['id'] for r in response]  # store ids of all matched data
    num_page = int(len(result_id) / ONE_PAGE) + 1 if len(result_id) % ONE_PAGE != 0 else int(
        len(result_id) / ONE_PAGE)  # calculates total number of pages possible
    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not

    results = process_result_display(response)
    result_display = results[:ONE_PAGE]
    return render_template("results.html", query_text=query_text,
                           sort=sort, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    # read in values
    query_text = request.form['query_text']
    result_id_raw = request.form['result_id']
    result_id = ast.literal_eval(result_id_raw)
    num_page_raw = request.form['num_page']
    num_page = int(num_page_raw) if num_page_raw != "" else 0
    results_raw = request.form['results']
    results = ast.literal_eval(results_raw)

    prev_disabled = True if page_id == 1 else False
    next_disabled = True if page_id == num_page else False

    start_index = (page_id - 1) * ONE_PAGE
    end_index = None if next_disabled else page_id * ONE_PAGE

    result_display = results[start_index:end_index]  # retrieve ids of doc to be displayed in this page

    return render_template("results.html", query_text=query_text,
                           sort=None, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


# ************************************************
# health search pages;
# ************************************************
@app.route("/health_search")
def health_search():
    return render_template("health_search.html")


@app.route("/health_search/results", methods=["POST"])
def health_results():
    global response
    global nutrition_options
    global cuisine
    global sort
    global order

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query_text"]
    sort = request.form["sort"]
    cuisine = request.form["cuisine"]  # cuisine (all, chinese, ...)
    order = request.form["order"]  # order (desc, asc)

    query = Match(title={"query": query_text})
    response = health_search(index_name, query, top_k, cuisine, sort, order)

    page_id = 1  # set page id to be 1
    result_id = [r['id'] for r in response]  # store ids of all matched data
    num_page = int(len(result_id) / ONE_PAGE) + 1 if len(result_id) % ONE_PAGE != 0 else int(
        len(result_id) / ONE_PAGE)  # calculates total number of pages possible
    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not

    results = process_result_display(response)
    result_display = results[:ONE_PAGE]
    return render_template("health_results.html", query_text=query_text,
                           sort=sort, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/health_search/results/<int:page_id>", methods=["POST"])
def health_next_page(page_id):
    # read in values
    query_text = request.form['query_text']
    result_id_raw = request.form['result_id']
    result_id = ast.literal_eval(result_id_raw)
    num_page_raw = request.form['num_page']
    num_page = int(num_page_raw) if num_page_raw != "" else 0
    results_raw = request.form['results']
    results = ast.literal_eval(results_raw)

    prev_disabled = True if page_id == 1 else False
    next_disabled = True if page_id == num_page else False

    start_index = (page_id - 1) * ONE_PAGE
    end_index = None if next_disabled else page_id * ONE_PAGE

    result_display = results[start_index:end_index]  # retrieve ids of doc to be displayed in this page

    return render_template("health_results.html", query_text=query_text,
                           sort=None, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/doc/<doc_id>")
def doc(doc_id):
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query = Match(id={"query": doc_id})
    # !!! Definitely need improvement
    doc = [_ for _ in default_search(index_name, query, top_k, cuisine, sort, order)]
    doc = doc[0].to_dict()
    return render_template("doc.html", doc=doc)

@app.route("/health_doc/<doc_id>")
def health_doc(doc_id):
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query = Match(id={"query": doc_id})
    # !!! Definitely need improvement
    doc = [_ for _ in health_search(index_name, query, top_k, cuisine, sort, order)]
    doc = doc[0].to_dict()
    return render_template("doc.html", doc=doc)


# ************************************************
# Helper methods
# ************************************************
def default_search(index: str, query: Query, top_k, cuisine, sort, order) -> None:
    s = Search(using="default", index=index)
    if cuisine != "all":
        s = s.filter('term', cuisine=cuisine)
    s = s.query(query)
    if sort != "default":
        s = s.sort({sort: {"order": order}})
    s = s[:top_k]
    r = s.execute()
    return r


def health_search(index: str, query: Query, top_k, cuisine, sort, order) -> None:
    s = Search(using="default", index=index)
    if cuisine != "all":
        s = s.filter('term', cuisine=cuisine)
    s = s.query(query)
    if sort != "default":
        sort = nutrition_options[sort]
        s = s.sort({sort: {"order": order}})
    s = s[:top_k]
    r = s.execute()
    return r


def process_result_display(response: List) -> List:
    results = []  # store processed content block
    for result in response:
        result = result.to_dict()
        result_dict = {}
        result_dict['id'] = result['id']
        result_dict['title'] = result['title']
        result_dict['health'] = result['fsa_lights_per100g']
        result_dict['ingredients'] = list(result['ingredients'].keys()) if result['ingredients'] != "" else []
        result_dict['ingredients_description'] = [val['description'] for val in result['ingredients'].values()]
        result_dict['complexity'] = len(result['instructions'].keys())
        results.append(result_dict)
    return results


if __name__ == "__main__":
    app.run(debug=True, port=5000)
