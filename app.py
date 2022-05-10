import ast
from flask import Flask, render_template, request
from typing import List, Dict
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Match, MatchAll, ScriptScore, Ids, Query
from elasticsearch_dsl.connections import connections

# ************************************************
# Author:
# routing methods: Tianjun Cai
# search methods: Alicia Sheng
# ************************************************

app = Flask(__name__)
index_name = "cooking_recipe"  # name of es index
top_k = 20  # define number of documents demonstrated
ONE_PAGE = 8  # maximum number of snippets on one page
response = []  # stores list of es search results
nutrition_options = {"energy": "nutr_values_per100g_energy",
                     "fat": "nutr_values_per100g_fat",
                     "protein": "nutr_values_per100g_protein",
                     "salt": "nutr_values_per100g_salt",
                     "saturates": "nutr_values_per100g_saturates",
                     "sugars": "nutr_values_per100g_sugars"}  # maps nutr values to es values


# ************************************************
# general search pages;
# ************************************************
@app.route("/")
def home():
    """
    home page, for general search
    :return: template of home.html
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    """
    results page, for general search
    :return: template of results.html
    """
    global response  # use global variable response to store search results

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # connect to ES
    query_text = request.form["query_text"]  # user query input
    sort = request.form["sort"]  # user search type: complexity, healthiness, ingredients
    cuisine = request.form["cuisine"]  # user search cuisine: all, chinese, ...
    order = request.form["order"]  # result display order: desc, asc

    if sort == "ingredients":  # if sort by ingredients
        query = Match(ingredients_plain_text={"query": query_text})  # match with ingredients_plain_text
    else:
        query = Match(title={"query": query_text})  # match with title of recipes
    response = default_search(index_name, query, top_k, cuisine, sort, order, query_text)  # search es and stores results in response

    page_id = 1  # set page id to be 1
    result_id = [r['id'] for r in response]  # store ids of all matched data
    num_page = int(len(result_id) / ONE_PAGE) + 1 if len(result_id) % ONE_PAGE != 0 else int(
        len(result_id) / ONE_PAGE)  # calculates total number of pages possible
    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not

    results = process_result_display(response)  # process results data and only leave information need for results page
    result_display = results[:ONE_PAGE]  # stores first ONE_PAGE number of results for display purpose
    return render_template("results.html", query_text=query_text,
                           sort=sort, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    next_page functionality, for general search
    :return: template of results.html, with new page_id
    """
    # read in values
    query_text = request.form['query_text']  # acquire user input
    result_id_raw = request.form['result_id']  # acquire results id
    result_id = ast.literal_eval(result_id_raw)  # convert string format of results id to list
    num_page_raw = request.form['num_page']  # acquire number of total pages
    num_page = int(num_page_raw) if num_page_raw != "" else 0  # convert string format of num of pages to int
    results_raw = request.form['results']  # acquire results
    results = ast.literal_eval(results_raw)  # convert string format of results to list

    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not
    start_index = (page_id - 1) * ONE_PAGE  # calculates start index for current page display
    end_index = None if next_disabled else page_id * ONE_PAGE  # calculates end index for current page display

    result_display = results[start_index:end_index]  # retrieve ids of doc to be displayed in this page
    return render_template("results.html", query_text=query_text,
                           sort=None, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/doc/<doc_id>")
def doc(doc_id):
    """
    doc, for general search
    :param: doc_id, in string format
    :return: template of doc.html
    """
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # connect to es
    s = Search(using="default", index=index_name).query(Match(id={"query": doc_id}))  # search es for this doc information
    r = s.execute()  # search for results
    doc = r[0].to_dict()  # convert retrieved data to dictionary format
    return render_template("doc.html", doc=doc)


# ************************************************
# health search pages;
# ************************************************
@app.route("/health_search")
def health_search():
    """
    health_search, for health search
    :return: template of health_search.html
    """
    return render_template("health_search.html")


@app.route("/health_search/results", methods=["POST"])
def health_results():
    """
    health_results, for health search
    :return: template of health_results.html
    """
    global response  # acquire global variable response to store results

    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # connect to es
    query_text = request.form["query_text"]  # acquire user query
    sort = request.form["sort"]  # acquire user search type
    cuisine = request.form["cuisine"]  # acquire user desired cuisine (all, chinese, ...)
    order = request.form["order"]  # acquire user desired order (desc, asc)

    # searching with specific numeric value in advanced & customized search
    # The following section seems confusing at first, yet the goal is to generate a raw dict containing the search body
    # that could be used to construct a new Search instance.
    # Following website contains some relevant information (under Search.from_dict()):
    # https://elasticsearch-dsl.readthedocs.io/en/latest/api.html
    # example search body:
    # {
    #     "query": {
    #         "bool": {
    #             "must": [
    #                 {
    #                     "match": {
    #                         "title": query_text
    #                     }
    #                 },
    #                 {
    #                     "range": {
    #                         "nutr_values_per100g_fat": {
    #                             "lte": 10
    #                         }
    #                     }
    #                 }
    #             ]
    #         }
    #     }
    # }
    nutr_num_search = False  # determines if user use advanced nutr num search
    match_dict = {"match": {"title": query_text}}  # generates match section in search body
    search_strategy = {'query': {}}  # initiates a search body
    search_strategy['query']['bool'] = {}  # adds bool in search body
    search_strategy['query']['bool']['must'] = []  # adds must in search body
    search_strategy['query']['bool']['must'].append(match_dict)  # append match section into search body
    for nutr, key in nutrition_options.items():  # iterate through nutrition options and check there is user input
        nutr_min = float(request.form[nutr + "_min"])  # acquire min value of nutr
        nutr_max = float(request.form[nutr + "_max"])  # acquire max value of nutr
        nutr_gt_lt = {key: {"gte": nutr_min}}  # stores nutr min search strategy
        if nutr_min != 0:  # if min value is not 0, i.e. user has their inputs
            nutr_num_search = True  # if at least one min value has been set, then set to True
        if nutr_max != 0:  # if haven't set value for max
            nutr_gt_lt[key]["lte"] = nutr_max  # stores nutr max search strategy
            nutr_num_search = True  # if at least one max value has been set, then set to True
        nutr_strategy = {'range': nutr_gt_lt}  # adds nutr min and max search strategy to range
        search_strategy['query']['bool']['must'].append(nutr_strategy)  # append nutr search strategy to search body

    if nutr_num_search:  # if search by nutr numeric values (i.e. users have input)
        response = health_nutr_num_search(search_strategy, top_k, cuisine, sort, order, query_text)  # stores results in response
    else:  # if user does not use numeric values search
        query = Match(title={"query": query_text})  # generate query for search
        response = health_search_algo(index_name, query, top_k, cuisine, sort, order, query_text)  # stores results in response

    page_id = 1  # set page id to be 1
    result_id = [r['id'] for r in response]  # store ids of all matched data
    num_page = int(len(result_id) / ONE_PAGE) + 1 if len(result_id) % ONE_PAGE != 0 else int(
        len(result_id) / ONE_PAGE)  # calculates total number of pages possible
    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not

    results = process_result_display(response)  # process results data and only leave information need for results page
    result_display = results[:ONE_PAGE]  # stores first ONE_PAGE number of results for display purpose
    return render_template("health_results.html", query_text=query_text,
                           sort=sort, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/health_search/results/<int:page_id>", methods=["POST"])
def health_next_page(page_id):
    """
    health_next_page, for health search
    :param: page_id, int
    :return: template of health_results.html
    """
    # read in values
    query_text = request.form['query_text']  # acquire user query
    result_id_raw = request.form['result_id']  # acquire results id in string format
    result_id = ast.literal_eval(result_id_raw)  # convert results is to list
    num_page_raw = request.form['num_page']  # acquire num of pages in string format
    num_page = int(num_page_raw) if num_page_raw != "" else 0  # converts num of pages to int
    results_raw = request.form['results']  # acquire results in string format
    results = ast.literal_eval(results_raw)  # convert results into list

    prev_disabled = True if page_id == 1 else False  # True if prev button disabled, false if not
    next_disabled = True if page_id == num_page else False  # True if next button disabled, false if not
    start_index = (page_id - 1) * ONE_PAGE  # calculates start index for current page display
    end_index = None if next_disabled else page_id * ONE_PAGE  # calculates end index for current page display

    result_display = results[start_index:end_index]  # retrieve ids of doc to be displayed in this page

    return render_template("health_results.html", query_text=query_text,
                           sort=None, results=results, doc=result_display,
                           result_id=result_id, page_id=page_id, num_page=num_page,
                           prev_disabled=prev_disabled, next_disabled=next_disabled)


@app.route("/health_search/doc/<doc_id>")
def health_doc(doc_id):
    """
    health_doc, for health search
    :param: doc_id, in string format
    :return: template of health_doc.html
    """
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")  # connect to es
    s = Search(using="default", index=index_name).query(Match(id={"query": doc_id}))  # search strategy
    r = s.execute()  # search es
    doc = r[0].to_dict()  # convert results into dictionary form
    return render_template("health_doc.html", doc=doc)


# ************************************************
# Helper methods
# ************************************************
def default_search(index: str, query: Query, top_k: int, cuisine: str, sort: str, order: str, query_text: str) -> None:
    """
    provide functionality to search es
    :param index: index name
    :param query: query instance for search
    :param top_k: top_k results stored in list
    :param cuisine: cuisine to filter on
    :param sort: type of emphasis (complexity, healthiness) to be sorted on
    :param order: desc or asc, order of results display
    :param query_text: user input query
    """
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
    """
    provide functionality to search es
    :param index: index name
    :param query: query instance for search
    :param top_k: top_k results stored in list
    :param cuisine: cuisine to filter on
    :param sort: type of nutr to be sorted
    :param order: desc or asc, order of results display
    :param query_text: user input query
    """
    s = Search(using="default", index=index)  # construct Search instance
    if cuisine != "all":  # if user has specified cuisine
        s = s.filter('term', cuisine=cuisine)  # filter on specified cuisine
    if query_text != "":  # if user does not have empty query
        s = s.query(query)  # query with Query instance
    if sort != "default":  # if user has specified nutrition to sort on
        sort = nutrition_options[sort]  # retrieve corresponding es key for sort
        s = s.sort({sort: {"order": order}})  # sort based on nutr and order (desc, asc)
    s = s[:top_k]  # get top_k of results
    r = s.execute()  # execute search
    return r


def health_nutr_num_search(strategy: Dict, top_k: int, cuisine: str, sort: str, order: str, query_text: str) -> None:
    """
    provide functionality to search es when user use advanced & customized search in health search
    :param strategy: strategy for search on numeric values
    :param top_k: top_k results stored in list
    :param cuisine: cuisine to filter on
    :param sort: type of nutr to be sorted
    :param order: desc or asc, order of results display
    :param query_text: user input query
    """
    if query_text == "":  # if empty query
        strategy["query"]["bool"]["must"].pop(0)  # remove search by query strategy from search body
    s = Search.from_dict(strategy)  # construct new Search instance from strategy
    if cuisine != "all":  # if user choose one cuisine
        s = s.filter('term', cuisine=cuisine)  # filter with this cuisine
    if sort != "default":  # if user choose one nutr for ranking
        sort = nutrition_options[sort]  # retrieve corresponding es key for sort
        s = s.sort({sort: {"order": order}})  # sort based on nutr and order (desc, asc)
    s = s[:top_k]  # get top_k of results
    r = s.execute()  # execute search
    return r


def process_result_display(response: List) -> List:
    """
    process results for display
    :param: response list to be comprehensive result list
    """
    results = []  # store processed content block
    for result in response:  # iterate through response list
        result = result.to_dict()  # convert response to dictionary
        result_dict = {}  # create new dictionary to store processed data
        result_dict['id'] = result['id']
        result_dict['title'] = result['title']
        result_dict['health'] = result['fsa_lights_per100g']
        result_dict['ingredients'] = list(result['ingredients'].keys()) if result['ingredients'] != "" else []  # store only ingredients' names
        result_dict['complexity'] = len(result['instructions'].keys())  # store length of instructions as complexity
        raw_cuisine = result['cuisine']
        # process cuisine input
        final_cuisine = raw_cuisine  # process cuisine display
        if raw_cuisine == "southern_us":
            final_cuisine = "Southern US"
        elif raw_cuisine == "cajun_creole":
            final_cuisine = "Cajun Creole"
        else:
            final_cuisine = final_cuisine.capitalize()
        result_dict['cuisine'] = final_cuisine
        results.append(result_dict)  # append result_dict to results
    return results


if __name__ == "__main__":
    app.run(debug=True, port=5000)
