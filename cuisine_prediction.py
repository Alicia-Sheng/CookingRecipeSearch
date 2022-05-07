from time import time

import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold
from sklearn.svm import SVC

names = [
#         'GradientBoostingRegressor',
        'LDA',
#         'Nearest Neighbors',
        'AdaBoostClassifier',
        'RandomForest',
        "Linear SVM",
        "RBF SVM",
#         "Decision Tree",
        "sLDA",
#         "MLP",
#         'RUSBoost',
        ]

# build classifiers
classifiers = [
#             GradientBoostingRegressor(random_state=1),
            LinearDiscriminantAnalysis(),
#             KNeighborsClassifier(n_neighbors=4),
            AdaBoostClassifier(n_estimators=400, learning_rate = 0.6),
            RandomForestClassifier(),
            SVC(kernel="linear", C=0.025),
            SVC(gamma=2, C=1),
#             DecisionTreeClassifier(),
            LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto'),
#             MLPClassifier(random_state=1, max_iter=300),
#             RUSBoostClassifier(n_estimators = 200, random_state=1),
              ]

df = pd.read_csv("data/embedded_whats_cooking/embedded_train.csv")

y_labels = df["label"].tolist()

print(set(y_labels))

print(len(set(y_labels)))

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
df = df.drop(['label', 'id'], axis=1)
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]
print(df)

scoring = "accuracy"
data = df.to_numpy()
X = data[:, 1:]
y = data[:, 0]

score_dict = {}
time_dict = {}
models = zip(names, classifiers)

for name, model in models:
    print("The model running is: " + name)
    time_start = time()
    kfold = RepeatedStratifiedKFold()
    scores = cross_val_score(model, X, y, cv=kfold, scoring=scoring)
    time_end = time()
    score_dict[name] = scores.mean()
    time_elapsed = time_end - time_start
    time_dict[name] = time_elapsed
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
df_record.to_csv("output/classifiers_accuracy_runtime.csv")