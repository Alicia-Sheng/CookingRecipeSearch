# ************************************************
# Author: Gordon Dou
# Date: May 9th, 2022
# Description: this class runs stratified k-fold cross-validation on LDA, KNN, Random Forest, SVM, Decision Tree, and MLP.
# Adaboost, shrinkage LDA, SVM with RBF kernel function, Gradient Boost took extremely long time to execute
# and failed to yield output on our computer. The results of each classifier will be saved as a csv file in the
# output folder.
#
# side note: it took us over 20 hours to finish running all of the classfiers.
# ************************************************

from time import time

import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold


train_path = "data/embedded_whats_cooking/embedded_train.csv"
output_path = "output/classifiers_accuracy_runtime.csv"

# a list of names of classifiers that you execute
names = [
        'LDA',
        'Nearest Neighbors',
        # 'AdaBoostClassifier',
        'RandomForest',
        "Linear_SVM",
        # "RBF_SVM",
        "Decision Tree",
        # "sLDA",
        "MLP",
#         'GradientBoostingRegressor',
#         'RUSBoost',
        ]

# build a list of corresponding classifiers that match the names of classifiers
classifiers = [
            LinearDiscriminantAnalysis(),
            KNeighborsClassifier(n_neighbors=20),
            # AdaBoostClassifier(n_estimators=400, learning_rate = 0.6),
            RandomForestClassifier(),
            SVC(kernel="linear", C=0.025),
            # SVC(gamma=2, C=1),
            DecisionTreeClassifier(),
            # LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto'),
            MLPClassifier(random_state=1, max_iter=300),
#             GradientBoostingRegressor(random_state=1),
#             RUSBoostClassifier(n_estimators = 200, random_state=1),
              ]

# dataframe for loading training dataset
df = pd.read_csv(train_path)

y_labels = df["label"].tolist() # a list of true labels

print(set(y_labels))

print(len(set(y_labels)))

# Create a dictionary that maps true labels into an integer in the range 0 - 19
label_dict = {}

count = 0
for ele in set(y_labels):
    label_dict[ele] = count
    count += 1
print("="*20)
print(label_dict)

encoded_labels = []
for label in y_labels:
    encoded_labels.append(label_dict[label])
print(len(encoded_labels))
print(encoded_labels[:20])

df["y"] = encoded_labels
df = df.drop(['label', 'id'], axis=1) # cleaned up the dataframe
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols] # rearranged the dataframe so that labels are in the first column
print(df)

scoring = "accuracy" # the cross validation scoring methods (we just focused on the accuracy)
data = df.to_numpy()
X = data[:, 1:]
y = data[:, 0]

score_dict = {}
time_dict = {}
models = zip(names, classifiers)

# Start running different classifiers
for name, model in models:
    print("The model running is: " + name)
    time_start = time() #the starting time of the classifier
    kfold = RepeatedStratifiedKFold() # an object for repeated stratified k fold
    scores = cross_val_score(model, X, y, cv=kfold, scoring=scoring) # performs cross validation
    time_end = time() # the ending time of the classifier
    score_dict[name] = scores.mean() # we use the average accuracy as the accuracy of the classifier
    time_elapsed = time_end - time_start
    time_dict[name] = time_elapsed

    tp_data = {"Average_Accuracy": scores.mean(), "Avg runtime(s)": time_elapsed}
    df_tp = pd.DataFrame(tp_data, index=[name])
    df_tp.to_csv("output/"+name+"_accuracy_runtime.csv")

    print("The average score of " + name + " is", scores.mean(), "with std of", scores.std())
    print("Time to run " + name + " is", str(time_elapsed))
    print("=" * 20)

print("score_dict is", score_dict)
print("time_dict is", time_dict)

classifier_name = names
accuracy_list = []
time_list = []
for name in classifier_name:
    accuracy_list.append(score_dict[name])
    time_list.append(time_dict[name])
recording = {"Accuracy": accuracy_list, "Runtime(s)":time_list}

df_record = pd.DataFrame(recording, index = classifier_name)
df_record.to_csv(output_path) # save the accuracy and the runtime of each classifier as a CSV file