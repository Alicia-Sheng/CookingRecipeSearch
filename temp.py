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
with open('temp_data_json.json', 'w') as f:
    json.dump(data, f, indent=4, separators=(',', ':'))
f.close()


# ************************************************
# output new data
new_data = """[{'id': '000095fc1d', 'title': 'Yogurt Parfaits', 'instructions': {0: 'Layer all ingredients in a serving dish.'}, 'instructions_length': 1, 'fsa_lights_per100g': 
{'fat': 'green', 'salt': 'green', 'saturates': 'green', 'sugars': 'orange'}, 'healthiness': 3, 'ingredients': {'yogurt': {'description': 'greek, plain, nonfat', 'quantity': '8 ounce', 'nutr_per_ingredient': {'fat': 0.8845044000000001, 'nrg': 133.80964, 'pro': 23.110512399999998, 'sat': 0.26535132, 'sod': 81.64656, 'sug': 7.348190400000001}}, 'strawberries': {'description': 'raw', 'quantity': '1 cup', 'nutr_per_ingredient': {'fat': 0.46, 'nrg': 49.0, 'pro': 1.02, 'sat': 0.023, 'sod': 2.0, 'sug': 7.43}}, 'cereals ready-to-eat': {'description': 'granola, homemade', 'quantity': '1/4 cup', 'nutr_per_ingredient': {'fat': 7.415, 'nrg': 149.25, 'pro': 4.17, 'sat': 1.207, 'sod': 8.0, 'sug': 6.04}}}, 'ingredients_plain_text': 'yogurt: greek, plain, nonfat; strawberries: raw; cereals ready-to-eat: granola, homemade; ', 'nutr_values_per100g': {'energy': 81.12946131894766, 'fat': 2.140139263515891, 'protein': 6.914436593565536, 'salt': 0.05597816738985967, 'saturates': 0.36534716195613937, 'sugars': 5.08634103436144}, 'nutr_values_per100g_energy': 81.12946131894766, 'nutr_values_per100g_fat': 2.140139263515891, 'nutr_values_per100g_protein': 6.914436593565536, 'nutr_values_per100g_salt': 0.05597816738985967, 'nutr_values_per100g_saturates': 0.36534716195613937, 'nutr_values_per100g_sugars': 5.08634103436144, 'url': 'http://tastykitchen.com/recipes/breakfastbrunch/yogurt-parfaits/'},
{'id': '00051d5b9d', 'title': 'Salt Free, Low Cholesterol Sugar Cookies Recipe', 'instructions': {0: 'Cream sugar and butter together till smooth.', 1: 'Add in egg beaters, orange rind, orange juice, and mix well.', 2: 'Mix together low sodium baking powder and flour.', 3: 'Add in to creamed mix and mix well.', 4: 'Roll dough into 1 inch balls and place on ungreased cookie sheet.', 5: 'Rub small amount of salt free butter on bottom of glass.', 6: 'Dip glass in granulated sugar.', 7: 'Flatten cookie dough ball slightly using flat end of glass.', 8: 'Bake at 300 degrees for 10-12 min.'}, 'instructions_length': 9, 'fsa_lights_per100g': {'fat': 'red', 'salt': 'orange', 'saturates': 'orange', 'sugars': 'orange'}, 'healthiness': -1, 'ingredients': {'sugars': {'description': 'granulated', 'quantity': '1/2 cup', 'nutr_per_ingredient': {'fat': 0.0, 'nrg': 384.0, 'pro': 0.0, 'sat': 0.0, 'sod': 0.0, 'sug': 100.56000000000002}}, 'oil': {'description': 'corn, peanut, and olive', 'quantity': '3/4 cup', 'nutr_per_ingredient': {'fat': 168.0, 'nrg': 1488.0, 'pro': 0.0, 'sat': 24.132, 'sod': 0.0, 'sug': 0.0}}, 'egg substitute': {'description': 'powder', 'quantity': '1/4 cup', 'nutr_per_ingredient': {'fat': 2.7625, 'nrg': 94.35000000000001, 'pro': 11.793750000000001, 'sat': 0.800275, 'sod': 170.0, 'sug': 4.6325}}, 'orange juice': {'description': 'raw', 'quantity': '1/4 teaspoon', 'nutr_per_ingredient': {'fat': 0.0026041666666666665, 'nrg': 0.5833333333333333, 'pro': 0.0090625, 'sat': 0.00031249999999999995, 'sod': 0.010416666666666666, 'sug': 0.10848958333333332}}, 'leavening agents': {'description': 'baking powder, double-acting, sodium aluminum sulfate', 'quantity': '1 tablespoon', 'nutr_per_ingredient': {'fat': 0.0, 'nrg': 6.0, 'pro': 0.0, 'sat': 0.0, 'sod': 1464.0, 'sug': 0.0}}, 'wheat flour': {'description': 'white, all-purpose, unenriched', 'quantity': '3 1/2 cup', 'nutr_per_ingredient': {'fat': 4.305, 'nrg': 1592.5, 'pro': 45.185, 'sat': 0.679, 'sod': 7.0, 'sug': 1.1900000000000002}}}, 'ingredients_plain_text': 'sugars: granulated; oil: corn, peanut, and olive; egg substitute: powder; orange juice: raw; orange juice: raw; leavening agents: baking powder, double-acting, sodium aluminum sulfate; wheat flour: white, all-purpose, unenriched; ', 'nutr_values_per100g': {'energy': 477.09640393594606, 'fat': 23.412485931109796, 'protein': 7.625491714677334, 'salt': 0.5486205522805532, 'saturates': 3.4250537682338384, 'sugars': 14.298442949953758}, 'nutr_values_per100g_energy': 477.09640393594606, 'nutr_values_per100g_fat': 23.412485931109796, 'nutr_values_per100g_protein': 7.625491714677334, 'nutr_values_per100g_salt': 0.5486205522805532, 'nutr_values_per100g_saturates': 3.4250537682338384, 'nutr_values_per100g_sugars': 14.298442949953758, 'url': 'http://cookeatshare.com/recipes/salt-free-low-cholesterol-sugar-cookies-6256'}]"""

new_data_pure = ast.literal_eval(new_data)
with open('temp_new_data_json.json', 'w') as f:
    json.dump(new_data_pure, f, indent=4, separators=(',', ':'))
f.close()