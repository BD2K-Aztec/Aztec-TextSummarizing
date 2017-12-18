import os, sys
import wordsegment as ws
import pandas as pd
import numpy as np
import csv

# created by Duan Li dxl360@cs.ucla.edu

# update the training model:
# give negative label once detecting stopwords including recently,existing and etc.

RESULT_DIR = "../result/"
RESULT_FILE = RESULT_DIR + "output_1.csv"
OUTPUT_FILE = RESULT_DIR + "output_2.csv"

df1 = pd.read_csv(RESULT_FILE)
article_data = df1.article
sentence_data = df1.sentence
label_data = df1.label

REF_VOCAB_DIR = "../ref/stopwords.txt"
with open(REF_VOCAB_DIR, "r") as fin:
    lines = fin.readlines()
stopwords = set([kw.strip() for kw in lines if len(kw.strip()) > 0])
count = 0
with open(OUTPUT_FILE, "w") as fout:
    fieldnames = ['article', 'sentence', 'label']
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(sentence_data)):
        text_precess = sentence_data[i].lower().replace("/", " ").replace(", ", " ").replace(": ", " ")
        set_text = set(text_precess.strip().split())
        if len(set_text & stopwords) > 0:
            writer.writerow({'article': article_data[i], 'sentence': sentence_data[i], 'label': 0})
            count +=1
            print(sentence_data[i])
        else :
            writer.writerow({'article': article_data[i], 'sentence': sentence_data[i], 'label': label_data[i]})
print(count)
