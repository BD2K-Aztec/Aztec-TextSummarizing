import os, sys
import wordsegment as ws
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import precision_score, recall_score, f1_score

"""
Text Summarization

Use manually labeled 100 articles as training data
    train the multinomial naive bayes and SVM models 
    to predict the rest of articles.
    
Negative samples are added since in the annotated text,
    the "1"s are way more than "0"s.

Created by Duan Li <dxl360@cs.ucla.edu> 
       and Zeyu Li <zyli@cs.ucla.edu>
"""

DATA_DIR = "../data2/"
INPUT_FILE = DATA_DIR + "labeled.txt"
TRAIN_FILE = DATA_DIR + "train.csv"
TEST_FILE = DATA_DIR + "output_1.csv"

# Load annotated text strings and labels from `labeled.txt`.
# Reformat the data into `sen` and `label`.
# If not loaded.
# if not os.path.exists(TRAIN_FILE):
with open(TRAIN_FILE, "w") as fout:
    fieldnames = ['sentence', 'label']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    with open(INPUT_FILE, "r",
              encoding="utf-8",
              errors='ignore') as fin:
        lines = fin.readlines()
        for line in lines:
            if line[0] != "=" \
                    and line[0] != "\n" \
                    and line[0] != ".":
                sentence, label = line.split("\t")[0:2]
                # print(sentence)
                writer.writerow({'sentence': sentence.strip(),
                                 'label': label.strip()})

# Adding the negative samples
NEG_RAW_FILE = "../result/negative.txt"
NEG_LABEL_FILE = "../result/negative_label.txt"
with open(NEG_LABEL_FILE, "w") as fout:
    fieldnames = ['sentence', 'label']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    with open(NEG_RAW_FILE, "r",
              encoding="utf-8",
              errors='ignore') as fin:
        lines = fin.readlines()

        for line in lines:
            sentence = line.strip()
            sp = sentence.split(" ")[:40]
            sentence = " ".join(sp)
            if sentence:
                writer.writerow({'sentence': sentence.strip(),
                                 'label': "0"})
# Load training data and testing data
df = pd.read_csv(TRAIN_FILE)
data, target = df.sentence, df.label

df_neg = pd.read_csv(NEG_LABEL_FILE)
# print(df_neg)
df_neg_sample = df_neg.sample(frac=0.06)
data_neg, target_neg = df_neg_sample.sentence, df_neg_sample.label

new_data = pd.concat([data, data_neg])
new_target = pd.concat([target, target_neg])

X = new_data.as_matrix()
y = new_target.as_matrix()

# print(X)
#
# print(np.count_nonzero(y))
# print(y.shape)
# In `y`, we have 135 True and 63 False

# print(X)
# print(y)

# Generate negative samples

rs = ShuffleSplit(n_splits=10, test_size=.1, random_state=1993)
i = 0

for train_index, test_index in rs.split(X):
    train_X, train_y = X[train_index], y[train_index]
    test_X, test_y = X[test_index], y[test_index]

    # print(train_X.shape)
    # print(test_y.shape)
    # print(train_y.shape)
    # print(test_X.shape)



    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', BernoulliNB())])

    text_clf.fit(train_X, train_y)
    predicted = text_clf.predict(test_X)

    # print(test_y)
    # print(predicted)

    pres, rec, f1 = precision_score(test_y, predicted), \
                    recall_score(test_y, predicted), \
                    f1_score(test_y, predicted)

    print("Precision\t{}".format(str(pres)))
    print("Recall\t{}".format(str(rec)))
    print("F1 score\t{}".format(str(f1)))
    print()

    i += 1
