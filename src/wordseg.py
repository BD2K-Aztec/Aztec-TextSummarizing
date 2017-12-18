#!/home/ww8/anaconda3/bin/python3.6

# created by Zeyu Li "zyli@cs.ucla.edu"

# Use word segmentation to separate the wrongly concatenated words
#   Example: INTRODUCTIONa new method

import wordsegment
import os
import sys
import re

PLACEHOLDER = "zzzz"

def word_segmentation(text):
    word_list = text.split(" ")
    new_list = []
    for word in word_list:
        wordseg = wordsegment.segment(word)
        new_list += wordseg
    return " ".join(new_list)

def sentence_seg(sen):
    sen_split = sen.split(" ")
    for i in range(0, len(sen_split)):
        seg_list = wordsegment.segment(sen_split[i])
        if len(seg_list) > 1:
            sen_split.remove(sen_split[i])
            sen_split.insert(i, " ".join(seg_list))
    return " ".join(sen_split)

if __name__ == "__main__":
    DATA_DIR = "../data/"
    # DATA_DIR = "../data/"

    INPUT_DIR = DATA_DIR + "parsed_text/"
    # INPUT_DIR = DATA_DIR + "parsed_label_text/"
    INPUT_DIR = DATA_DIR + "test/"
    OUTPUT_DIR = DATA_DIR + "parsed_seg_text/"
    # OUTPUT_DIR = DATA_DIR + "what/"
    file_list = os.listdir(INPUT_DIR)
    idx, total = 0, len(file_list)
    idx = 0

    # Regex of URLs
    regex_url = \
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    for f in file_list:
        idx += 1
        if idx % 300 == 0:
            print(idx / total)
        with open(INPUT_DIR + f, "r") as fin:
            with open(OUTPUT_DIR + f, "w") as fout:
                fin_paras = fin.readlines()
                # print(fin_paras)
                # HERE: Replace URL with PLACEHOLDER
                for paras in fin_paras:
                    urls = re.findall(regex_url, paras)
                    paras = re.sub(regex_url, PLACEHOLDER, paras)
                    fin_sentence = paras.split(". ")
                    for i in range(0, len(fin_sentence)):
                        fin_sentence[i] = sentence_seg(fin_sentence[i])
                    segd_para = ". ".join(fin_sentence)
                    # Replace the PLACEHOLDER back to URL
                    for url in urls:
                        segd_para = re.sub(PLACEHOLDER, url, segd_para, count=1)

                    fout.write(segd_para + "\n")


