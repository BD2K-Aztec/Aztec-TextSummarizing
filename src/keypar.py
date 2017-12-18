#!/usr/bin/python3

# created by Zeyu Li "zyli@cs.ucla.edu", modified by Duan Li dxl360@cs.ucla.edu
# Extract the paragraph that has the keyphrases in it.

import os, sys
import wordsegment as ws

THRESHOLD = 1

def read_kw():
    REF_VOCAB_DIR = "./ref/software_vocab.txt"
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
    DATA_DIR = "./data/"
    PARSED_FILE_DIR = DATA_DIR + "parsed_seg_text/"
    # PARSED_FILE_DIR = DATA_DIR + "parsed_label_text/"
    RESULT_DIR = "./result/"
    RESULT_DIR = "/home/ww8/Dropbox/"
    RESULT_FILE = RESULT_DIR + "extracted.txt"
    file_list = os.listdir(PARSED_FILE_DIR)
    total = len(file_list)
    idx = 0
    print(KEYWORDS)
    with open(RESULT_FILE, "w") as fout:
        for file in file_list:
            # Open every file
            with open(PARSED_FILE_DIR + file, "r") as fin:
                idx += 1
                if idx % 300 ==0:
                    print("{}%".format(int(idx/total * 100)))
                fout.write("\n\n======" + file + "========\n")
                lines = fin.readlines()

                # Each line is a paragraph
                for line in lines:
                    line = line.replace("...", " ")
                    sentences = line.split(". ")
                    for sen in sentences:
                        if key_paragraph(sen, KEYWORDS) > THRESHOLD:
                            # fout.write(sen+". ")
                            fout.write(sen + ".\t0\n")
