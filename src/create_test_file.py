#!/home/ww8/anaconda3/bin/python3.6

# created by Duan Li dxl360@cs.ucla.edu
# create testing file for model based on manually labeled data
# extract the sentences that has the keyphrases in it and export them into csv file

import os, sys
import wordsegment as ws
import csv

THRESHOLD = 1

def read_kw():
    REF_VOCAB_DIR = "../ref/software_vocab.txt"
    with open(REF_VOCAB_DIR, "r") as fin:
        lines = fin.readlines()
    KEYWORD = set([kw.strip() for kw in lines if len(kw.strip()) > 0])
    return KEYWORD


def key_paragraph(text, kw_set):
    text_precess = text.lower().replace("/", " ").replace(", ", " ").replace(": ", " ")
    set_text = set(text_precess.strip().split())
    return len(set_text & kw_set)


if __name__ == '__main__':
    KEYWORDS = read_kw()
    DATA_DIR = "../data/"
    PARSED_FILE_DIR = DATA_DIR + "parsed_label_text/"
    RESULT_DIR = "../result/"
    RESULT_FILE = RESULT_DIR + "output_1.csv"
    file_list = os.listdir(PARSED_FILE_DIR)
    total = len(file_list)
    idx = 0
    print(KEYWORDS)
    count = 0
    with open(RESULT_FILE, "w") as fout:
        fieldnames = ['article', 'sentence', 'label']
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for file in file_list:
            # Open every file
            with open(PARSED_FILE_DIR + file, "r", encoding="utf-8", errors='ignore') as fin:
                idx += 1
                if idx % 300 ==0:
                    print("{}%".format(int(idx/total * 100)))
                lines = fin.readlines()
                # Each line is a paragraph
                for line in lines:
                    line = line.replace("...", " ")
                    sentences = line.split(". ")
                    for sen in sentences:
                        if key_paragraph(sen, KEYWORDS) > THRESHOLD:
                            writer.writerow({'article': file, 'sentence': sen, 'label': 0})




