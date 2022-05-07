from typing import Dict, Union, Generator
import os
import json
from embedding_service.client import EmbeddingClient
import csv


def load_train(
    doc_path: Union[str, os.PathLike]
) -> None:
    """
    load wapo docs as a generator
    :param wapo_jl_path:
    :return: yields each document as a dict
    """
    f = open(doc_path, encoding='utf-8')
    data = json.load(f)
    sbert_encoder = EmbeddingClient(
        host="localhost", embedding_type="sbert"
    )
    header = ["id"]
    header_feature = [i for i in range(768)]
    header.extend(header_feature)
    header.append("label")
    with open('data/embedded_whats_cooking/embedded_train.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            ingredients_plain_text = [""]
            for i in range(len(d["ingredients"])):
                if i == len(d["ingredients"]) - 1:
                    ingredients_plain_text[0] += d["ingredients"][i]
                else:
                    ingredients_plain_text[0] += (d["ingredients"][i] + '#')
            embedding = sbert_encoder.encode(ingredients_plain_text)[0]
            row = [d["id"]]
            row.extend(embedding)
            row.append(d["cuisine"])
            writer.writerow(row)

def load_doc(
    doc_path: Union[str, os.PathLike]
) -> None:
    """
    load wapo docs as a generator
    :param wapo_jl_path:
    :return: yields each document as a dict
    """
    f = open(doc_path, encoding='utf-8')
    data = json.load(f)
    sbert_encoder = EmbeddingClient(
        host="localhost", embedding_type="sbert"
    )
    header = ["id"]
    header_feature = [i for i in range(768)]
    header.extend(header_feature)
    with open('data/embedded_recipe.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for d in data:
            ingredients_plain_text = [""]
            for i in range(len(d["ingredients"])):
                ingredient = d["ingredients"][i]
                text = ingredient["text"]
                texts = text.split(",")
                ing = texts[0].strip()
                if i == len(d["ingredients"]) - 1:
                    ingredients_plain_text[0] += ing
                else:
                    ingredients_plain_text[0] += (ing + '#')
            embedding = sbert_encoder.encode(ingredients_plain_text)[0]
            row = [d["id"]]
            row.extend(embedding)
            writer.writerow(row)


if __name__ == "__main__":
    # load_train("data/whats-cooking/train.json")
    load_doc("data/recipes_with_nutritional_info.json")