#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Alicia Sheng
Date: May 9th, 2022
Description: load es index loads the recipe dataset and labels to the ES server
"""

import argparse
import time
from typing import List, Dict, Union, Iterator
from index import ESIndex
from utils import load_clean_doc
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


class IndexLoader:
    """
    load document index to Elasticsearch
    """

    def __init__(self, index, docs):

        self.index_name = index
        self.docs: Union[Iterator[Dict], List[Dict]] = docs

    def load(self) -> None:
        st = time.time()
        logger.info(f"Building index ...")
        ESIndex(self.index_name, self.docs)
        logger.info(
            f"=== Built {self.index_name} in {round(time.time() - st, 2)} seconds ==="
        )

    @classmethod
    def from_docs_jsonl(cls, index_name: str, docs_jsonl: str, label_csv: str) -> "IndexLoader":
        try:
            return IndexLoader(index_name, load_clean_doc(docs_jsonl, label_csv))
        except FileNotFoundError:
            raise Exception(f"Cannot find {docs_jsonl}/{label_csv}!")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--index_name",
        required=True,
        type=str,
        help="name of the ES index",
    )
    parser.add_argument(
        "--doc_path",
        required=True,
        type=str,
        help="path to the processed jsonline file",
    )
    parser.add_argument(
        "--label_path",
        required=True,
        type=str,
        help="path to the label file",
    )

    args = parser.parse_args()
    idx_loader = IndexLoader.from_docs_jsonl(args.index_name, args.doc_path, args.label_path)
    idx_loader.load()


if __name__ == "__main__":
    main() # python load_es_index.py --index_name cooking_recipe --doc_path data/recipes_with_nutritional_info.json --label_path output/SVM_predicted_label.csv

