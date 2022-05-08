# CookingRecipeSearch

Data: http://pic2recipe.csail.mit.edu/

## Cuisine Prediction 

We used stratified k fold cross validation to verify the following results.


| Classifier                | Average Accuracy | Average Runtime(s) |
|---------------------------|------------------|--------------------|
| SVM                       | 0.7208           | 18450.4            |
| LDA                       | 0.7148           | 194.7              |
| MLP                       | 0.6899           | 6491.4             |
| Nearest Neighbors         | 0.6725           | 301.5              |
| Random Forest             | 0.5965           | 8621.0             |
| Decision Tree             | 0.3768           | 2945.2             |
| GradientBoostingRegressor | -                | 49681.7            |
