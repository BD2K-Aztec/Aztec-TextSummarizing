import os, sys
import pandas as pd
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline

from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import precision_score, recall_score, f1_score
from word2vec import Word2Vec, Sent2Vec, LineSentence

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

D2V_DIR = "../d2v/"
D2V_SENT = D2V_DIR + "d2v_dat.txt"
D2V_LABEL = D2V_DIR + "d2v_label.txt"
D2V_MODEL = D2V_DIR + "w2v_model.model"
D2V_SENT_VEC = D2V_DIR + "d2v_dat.vec"

# Load annotated text strings and labels from `labeled.txt`.
# Reformat the data into `sen` and `label`.
def generate_train_data(frac):
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
    df_neg_sample = df_neg.sample(frac=frac)
    data_neg, target_neg = df_neg_sample.sentence, df_neg_sample.label

    new_data = pd.concat([data, data_neg])
    new_target = pd.concat([target, target_neg])

    X = new_data.as_matrix()
    y = new_target.as_matrix()

    with open(D2V_DIR + "d2v_dat.txt", "w") as fout_data, \
        open(D2V_DIR + "d2v_label.txt", "w") as fout_label:
        for x in X:
            fout_data.write(str(x) + "\n")
        for _y in y:
            fout_label.write(str(_y) + "\n")


def load_vec_file():
    with open(D2V_SENT_VEC, "r") as fin:
        lines = fin.readlines()
        vecs = [ [float(dim) for dim in line.split(" ")[1:] ]
                for line in lines[1:]]
    return vecs


def load_label_file():
    with open(D2V_LABEL, "r") as fin:
        lines = fin.readlines()
    return [int(x.strip()) for x in lines]


if __name__ == "__main__":
    if 1:
        generate_train_data(0.1)
    model = Sent2Vec(LineSentence(D2V_SENT),
                     model_file=D2V_MODEL)
    model.save_sent2vec_format(D2V_SENT_VEC)
    X = np.array(load_vec_file())
    y = np.array(load_label_file())
    rs = ShuffleSplit(n_splits=10,
                      test_size=.1,
                      random_state=1993)

    kernels = ['rbf', 'linear', 'poly', 'sigmoid']
    for kn in kernels:
        print(kn)
        for train_index, test_index in rs.split(X):
            train_X, train_y = X[train_index], y[train_index]
            test_X, test_y = X[test_index], y[test_index]
            text_clf = SVC(kernel=kn)
            text_clf.fit(train_X, train_y)
            predicted = text_clf.predict(test_X)

            pres, rec, f1 = precision_score(test_y, predicted), \
                            recall_score(test_y, predicted), \
                            f1_score(test_y, predicted)
            print("Precision\t{}".format(str(pres)))
            print("Recall\t{}".format(str(rec)))
            print("F1 score\t{}".format(str(f1)))



