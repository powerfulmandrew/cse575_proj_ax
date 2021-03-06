import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score             # grading
from sklearn.metrics import f1_score             # grading

# ******************************************************************************
# * Load data
# ******************************************************************************

data = pd.read_csv('cse575_project/cse575_proj_ax/cse575_proj_data/output.csv')  # filename
labels = data['koi_disposition'].to_numpy()
data = data.drop('koi_disposition', axis=1).to_numpy()

# generate kfolds
kf = KFold(n_splits=5, shuffle=True, random_state=0)

# for each kfold
i = 0

acc = []
mac = []
mic = []
wf1 = []

tp = []
tn = []
fp = []
fn = []

for train_index, test_index in kf.split(data, labels):
    x_train, x_test = data[train_index], data[test_index]
    y_train, y_test = labels[train_index], labels[test_index]

    model = LogisticRegression(C=7.1, solver='liblinear', multi_class='auto')
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    acc.append(accuracy_score(y_pred, y_test))
    mac.append(f1_score(y_test, y_pred, average="macro"))
    mic.append(f1_score(y_test, y_pred, average="micro"))
    wf1.append(f1_score(y_test, y_pred, average="weighted"))

    true_pos = 0
    true_neg = 0
    false_pos = 0
    false_neg = 0

    for j in range(y_test.shape[0]):
        if int(y_test[j]) == int(y_pred[j]):
            if int(y_pred[j]) == 1:
                true_pos += 1
            else:
                true_neg += 1
        else:
            if int(y_pred[j]) == 1:
                false_pos += 1
            else:
                false_neg += 1

    fp.append(false_pos)
    fn.append(false_neg)
    tp.append(true_pos)
    tn.append(true_neg)

print(f'Accuracy: {np.mean(acc)}')
print(f'Macro F1: {np.mean(mac)}')
print(f'Micro F1: {np.mean(mic)}')
print(f'Weighted F1: {np.mean(wf1)}')
print()
print(f'True +: {np.mean(tp)}')
print(f'True -: {np.mean(tn)}')
print(f'False +: {np.mean(fp)}')
print(f'False -: {np.mean(fn)}')
