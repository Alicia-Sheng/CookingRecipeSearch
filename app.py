import ast
from flask import Flask, render_template, request
from typing import List, Dict
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections

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

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query_text"]
    sort = request.form["sort"]  # sort (complexity, healthiness, fat, ...)
    cuisine = request.form["cuisine"]  # cuisine (all, chinese, ...)
    order = request.form["order"]  # order (desc, asc)

    if sort == "ingredients":
        query = Match(ingredients_plain_text={"query": query_text})
    else:
        query = Match(title={"query": query_text})
    response = default_search(index_name, query, top_k, cuisine, sort, order, query_text)

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


@app.route("/doc/<doc_id>")
def doc(doc_id):
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    s = Search(using="default", index=index_name).query(Match(id={"query": doc_id}))
    r = s.execute()
    doc = r[0].to_dict()
    return render_template("doc.html", doc=doc)


# ************************************************
# health search pages;
# ************************************************
@app.route("/health_search")
def health_search():
    return render_template("health_search.html")


@app.route("/health_search/results", methods=["POST"])
def health_results():
    global response

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query_text"]
    sort = request.form["sort"]
    cuisine = request.form["cuisine"]  # cuisine (all, chinese, ...)
    order = request.form["order"]  # order (desc, asc)

    nutr_num_search = False  # determines if user use advanced nutr num search
    nutr_num = {}
    match_dict = {"match": {"title": query_text}}
    search_strategy = {'query': {}}
    search_strategy['query']['bool'] = {}
    search_strategy['query']['bool']['must'] = []
    search_strategy['query']['bool']['must'].append(match_dict)
    for nutr, key in nutrition_options.items():
        nutr_min = int(request.form[nutr + "_min"])
        nutr_max = int(request.form[nutr + "_max"])
        nutr_num['nutr'] = tuple([nutr_min, nutr_max])
        nutr_gt_lt = {key: {"gte": nutr_min}}
        if nutr_min != 0:
            nutr_num_search = True  # if at least one min value has been set, then set to True
        if nutr_max != 0:  # if haven't set value for max
            nutr_gt_lt[key]["lte"] = nutr_max
            nutr_num_search = True  # if at least one max value has been set, then set to True
        nutr_strategy = {'range': nutr_gt_lt}
        search_strategy['query']['bool']['must'].append(nutr_strategy)

    if nutr_num_search:
        response = health_nutr_num_search(index_name, search_strategy, top_k, cuisine, sort, order, query_text)
    else:
        query = Match(title={"query": query_text})
        response = health_search_algo(index_name, query, top_k, cuisine, sort, order, query_text)

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


# @app.route("/health_search/results", methods=["POST"])
# def health_results():
#     global response
#
#     connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
#     query_text = request.form["query_text"]
#     sort = request.form["sort"]
#     cuisine = request.form["cuisine"]  # cuisine (all, chinese, ...)
#     order = request.form["order"]  # order (desc, asc)
#
#     query = Match(title={"query": query_text})
#     response = health_search_algo(index_name, query, top_k, cuisine, sort, order, query_text)
#
#     page_id = 1  # set page id to be 1
#     result_id = [r['id'] for r in response]  # store ids of all matched data
#     num_page = int(len(result_id) / ONE_PAGE) + 1 if len(result_id) % ONE_PAGE != 0 else int(
#         len(result_id) / ONE_PAGE)  # calculates total number of pages possible
#     prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
#     next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not
#
#     results = process_result_display(response)
#     result_display = results[:ONE_PAGE]
#     return render_template("health_results.html", query_text=query_text,
#                            sort=sort, results=results, doc=result_display,
#                            result_id=result_id, page_id=page_id, num_page=num_page,
#                            prev_disabled=prev_disabled, next_disabled=next_disabled)


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


@app.route("/health_search/doc/<doc_id>")
def health_doc(doc_id):
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    s = Search(using="default", index=index_name).query(Match(id={"query": doc_id}))
    r = s.execute()
    doc = r[0].to_dict()
    return render_template("health_doc.html", doc=doc)


# ************************************************
# Helper methods
# ************************************************
def default_search(index: str, query: Query, top_k: int, cuisine: str, sort: str, order: str, query_text: str) -> None:
    s = Search(using="default", index=index)
    if cuisine != "all":
        s = s.filter('term', cuisine=cuisine)
    if query_text != "":
        s = s.query(query)
    if sort != "default" and sort != "ingredients":
        s = s.sort({sort: {"order": order}})
    s = s[:top_k]
    r = s.execute()
    return r


def health_search_algo(index: str, query: Query, top_k: int, cuisine: str, sort: str, order: str, query_text: str) -> None:
    s = Search(using="default", index=index)
    if cuisine != "all":
        s = s.filter('term', cuisine=cuisine)
    if query_text != "":
        s = s.query(query)
    if sort != "default":
        sort = nutrition_options[sort]
        s = s.sort({sort: {"order": order}})
    s = s[:top_k]
    r = s.execute()
    return r


def health_nutr_num_search(index: str, strategy: Dict, top_k: int, cuisine: str, sort: str, order: str, query_text: str) -> None:
    if query_text == "":
        strategy["query"]["bool"]["must"].pop(0)  # remove search by query
    s = Search.from_dict(strategy)
    if cuisine != "all":
        s = s.filter('term', cuisine=cuisine)
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
        raw_cuisine = result['cuisine']
        # process cuisine input
        final_cuisine = raw_cuisine
        if raw_cuisine == "southern_us":
            final_cuisine = "Southern US"
        elif raw_cuisine == "cajun_creole":
            final_cuisine = "Cajun Creole"
        else:
            final_cuisine = final_cuisine.capitalize()
        result_dict['cuisine'] = final_cuisine
        results.append(result_dict)
    return results


if __name__ == "__main__":
    app.run(debug=True, port=5000)
