from typing import Dict, Union, Generator
import os
import json
import csv


def load_clean_doc(
        doc_path: Union[str, os.PathLike], label_path: Union[str, os.PathLike]
) -> Generator[Dict, None, None]:
    """
    load wapo docs as a generator
    :param doc_path:
    :return: yields each document as a dict
    """
    f = open(doc_path)
    data = json.load(f)
    with open(label_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)  # remove the header
        for d in data:
            doc = dict()
            doc["id"] = d["id"]
            output = next(reader)
            cuisine_id = output[0]
            label = output[1]
            if cuisine_id != d["id"]:
                print("ERROR!!!!!")
            doc["cuisine"] = label
            doc["title"] = d["title"]
            instruction = dict()
            for i in range(len(d["instructions"])):
                instruction_line = d["instructions"][i]
                instruction[i] = instruction_line["text"]
            doc["instructions"] = instruction
            doc["complexity"] = len(instruction)
            doc["fsa_lights_per100g"] = d["fsa_lights_per100g"]
            healthiness = 0
            for ingredient in d["fsa_lights_per100g"]:
                if d["fsa_lights_per100g"][ingredient] == "green":
                    healthiness += 1
                elif d["fsa_lights_per100g"][ingredient] == "red":
                    healthiness -= 1
            doc["healthiness"] = healthiness
            doc["ingredients"] = dict()
            ingredients_plain_text = ""
            for i in range(len(d["ingredients"])):
                ingredient_temp_plain = ""
                ingredient = d["ingredients"][i]
                text = ingredient["text"]
                texts = text.split(",")
                ing = texts[0].strip()
                ingredient_temp_plain += ing + ": "
                doc["ingredients"][ing] = dict()
                des = ""
                for j in range(1, len(texts)):
                    t = texts[j]
                    if j == len(texts) - 1:
                        des += t.strip()
                    else:
                        des += (t.strip() + ", ")
                ingredient_temp_plain += des + "; "
                ingredients_plain_text += ingredient_temp_plain
                doc["ingredients"][ing]["description"] = des
                quantity = d["quantity"][i]
                unit = d["unit"][i]
                q_u = quantity["text"] + " " + unit["text"]
                doc["ingredients"][ing]["quantity"] = q_u
                nutr = d["nutr_per_ingredient"][i]
                doc["ingredients"][ing]["nutr_per_ingredient"] = nutr
            doc["ingredients_plain_text"] = ingredients_plain_text
            doc["nutr_values_per100g"] = d["nutr_values_per100g"]
            doc["nutr_values_per100g_energy"] = d["nutr_values_per100g"]["energy"]
            doc["nutr_values_per100g_fat"] = d["nutr_values_per100g"]["fat"]
            doc["nutr_values_per100g_protein"] = d["nutr_values_per100g"]["protein"]
            doc["nutr_values_per100g_salt"] = d["nutr_values_per100g"]["salt"]
            doc["nutr_values_per100g_saturates"] = d["nutr_values_per100g"]["saturates"]
            doc["nutr_values_per100g_sugars"] = d["nutr_values_per100g"]["sugars"]
            doc["url"] = d["url"]
            yield doc


if __name__ == "__main__":
    # doc_path = "data/recipes_with_nutritional_info.json"
    # label_path = "output/SVM_predicted_label.csv"
    # gen = load_clean_doc(doc_path, label_path)
    # result = []
    # j = 0
    # for i in gen:
    #     print(i)
    #     result.append(i)
    #     j += 1
    #     if j == 2:
    #         break
    #
    # with open("temp/new_purified_data.json", "w") as f:
    #     json.dump(result, f, indent=4, separators=(',', ':'))
    # f.close()
    pass
