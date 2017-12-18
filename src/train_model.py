import os, sys
import wordsegment as ws
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# created by Duan Li dxl360@cs.ucla.edu

# use manually labeled 100 articles as training data
# train the multinomial naive bayes model to predict the rest of articles

RESULT_DIR = "../result/"
INPUT_FILE = RESULT_DIR + "labeled1_100.txt"
RESULT_FILE = RESULT_DIR + "train.csv"
TEST_FILE = RESULT_DIR + "output_1.csv"

with open(RESULT_FILE, "w") as fout:
    fieldnames = ['sentence', 'label']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    with open(INPUT_FILE, "r", encoding="utf-8", errors='ignore') as fin:
        lines = fin.readlines()
        for line in lines:
            if line[0] != "=" and line[0] != "\n":
                if line[0] != ".":
                    label = line.split("\t")[1]
                    sentence = line.split("\t")[0]
                    writer.writerow({'sentence': sentence, 'label': label})

# load training data and testing data
df = pd.read_csv(RESULT_FILE)
train_data = df.sentence
train_target = df.label
df1 = pd.read_csv(TEST_FILE)
test_data = df1.sentence
test_target = df1.label

# use multinomial naive bayes model to predict the label
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data)
print('training data shape is ', X_train_counts.shape)
X_train_counts = count_vect.fit_transform(test_data)
print('testing data shape is ', X_train_counts.shape)

text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])
text_clf.fit(train_data, train_target)
predicted = text_clf.predict(test_data)



