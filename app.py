import ast
from flask import Flask, render_template, request
from typing import List, Dict, Tuple

app = Flask(__name__)

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
    query_text = request.form["main_query"]
    fat = request.form["fat"]
    return render_template("results.html", query=query_text, fat=fat)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
