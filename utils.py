from typing import Dict, Union, Generator
import os
import json


def load_clean_wapo_with_embedding(
    wapo_jl_path: Union[str, os.PathLike]
) -> Generator[Dict, None, None]:
    """
    load wapo docs as a generator
    :param wapo_jl_path:
    :return: yields each document as a dict
    """
    f = open(wapo_jl_path)
    data = json.load(f)
    for d in data:
        doc = dict()
        doc["id"] = d["id"]
        doc["title"] = d["title"]
        instruction = dict()
        for i in range(len(d["instructions"])):
            instruction_line = d["instructions"][i]
            instruction[i] = instruction_line["text"]
        doc["instructions"] = instruction
        doc["fsa_lights_per100g"] = d["fsa_lights_per100g"]
        doc["ingredients"] = dict()
        for i in range(len(d["ingredients"])):
            ingredient = d["ingredients"][i]
            text = ingredient["text"]
            texts = text.split(",")
            ing = texts[0].strip()
            doc["ingredients"][ing] = dict()
            des = ""
            for j in range(1, len(texts)):
                t = texts[j]
                if j == len(texts) - 1:
                    des += t.strip()
                else:
                    des += (t.strip() + ", ")
            doc["ingredients"][ing]["description"] = des
            quantity = d["quantity"][i]
            unit = d["unit"][i]
            q_u = quantity["text"] + " " + unit["text"]
            doc["ingredients"][ing]["quantity"] = q_u
            nutr = d["nutr_per_ingredient"][i]
            doc["ingredients"][ing]["nutr_per_ingredient"] = nutr
        doc["nutr_values_per100g"] = d["nutr_values_per100g"]
        doc["url"] = d["url"]
        yield doc


if __name__ == "__main__":
    # load_clean_wapo_with_embedding("data/recipes_with_nutritional_info.json")
    pass