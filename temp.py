import json
import ast

data_example = """{'id': '000095fc1d', 'title': 'Yogurt Parfaits', 'instructions': {0: 'Layer all ingredients in a serving dish.'}, 'fsa_lights_per100g': {'fat': 'green', 
'salt': 'green', 'saturates': 'green', 'sugars': 'orange'}, 'ingredients': {'yogurt': {'description': 'greek, plain, nonfat', 'quantity': '8 ounce', 
'nutr_per_ingredient': {'fat': 0.8845044000000001, 'nrg': 133.80964, 'pro': 23.110512399999998, 'sat': 0.26535132, 'sod': 81.64656, 'sug': 7.348190400000001}}, 
'strawberries': {'description': 'raw', 'quantity': '1 cup', 'nutr_per_ingredient': {'fat': 0.46, 'nrg': 49.0, 'pro': 1.02, 'sat': 0.023, 'sod': 2.0, 
'sug': 7.43}}, 'cereals ready-to-eat': {'description': 'granola, homemade', 'quantity': '1/4 cup', 'nutr_per_ingredient': {'fat': 7.415, 'nrg': 149.25, 'pro': 4.17,
 'sat': 1.207, 'sod': 8.0, 'sug': 6.04}}}, 'nutr_values_per100g': {'energy': 81.12946131894766, 'fat': 2.140139263515891, 'protein': 6.914436593565536, 
 'salt': 0.05597816738985967, 'saturates': 0.36534716195613937, 'sugars': 5.08634103436144}, 
 'url': 'http://tastykitchen.com/recipes/breakfastbrunch/yogurt-parfaits/'}"""

data = ast.literal_eval(data_example)
print(data['ingredients'].keys())
a = dict()
print(a.keys())
print(type(a.keys()))
# with open('temp_data_json.json', 'w') as f:
#     json.dump(data, f, indent=4, separators=(',', ':'))
# f.close()

test_data = """[{'id': '5b086e2c79', 'title': 'Fried Chicken Chicken Salad', 'health': {'fat': 'orange', 'salt': 'red', 'saturates': 'green', 'sugars': 'green'}, 'ingredients': dict_keys(['chicken', 'celery', 'onions', 'salad dressing', 'salt', 'spices']), 'ingredients_description': ['broiler or fryers, breast, skinless, boneless, meat only, raw', 'raw', 'raw', 'mayonnaise, regular', 'table', 'pepper, black'], 'complexity': 4}, {'id': '3a7e09923f', 'title': "Mrs. Barber's Chicken (Chicken Stroganoff)", 'health': {'fat': 'orange', 'salt': 'red', 'saturates': 'orange', 'sugars': 'green'}, 'ingredients': dict_keys(['chicken', 'butter', 'salad dressing', 'cheese', 'soup']), 'ingredients_description': ['broiler or fryers, breast, skinless, boneless, meat only, raw', 'without salt', 'italian dressing, commercial, regular', 'parmesan, hard', 'cream of chicken, canned, condensed'], 'complexity': 8}]"""
# print(ast.literal_eval(test_data))
test_2 = """
[{'id': '5b086e2c79', 'title': 'Fried Chicken Chicken Salad', 'health': {'fat': 'orange', 'salt': 'red', 'saturates': 'green', 'sugars': 'green'}, 'ingredients': ['chicken', 'celery', 'onions', 'salad dressing', 'salt', 'spices'], 'ingredients_description': ['broiler or fryers, breast, skinless, boneless, meat only, raw', 'raw', 'raw', 'mayonnaise, regular', 'table', 'pepper, black'], 'complexity': 4}, {'id': '3a7e09923f', 'title': "Mrs. Barber's Chicken (Chicken Stroganoff)", 'health': {'fat': 'orange', 'salt': 'red', 'saturates': 'orange', 'sugars': 'green'}, 'ingredients': ['chicken', 'butter', 'salad dressing', 'cheese', 'soup'], 'ingredients_description': ['broiler or fryers, breast, skinless, boneless, meat only, raw', 'without salt', 'italian dressing, commercial, regular', 'parmesan, hard', 'cream of chicken, canned, condensed'], 'complexity': 8}"""
print(ast.literal_eval(test_2))
# test_json = json.loads(test_data)
# print(test_json)