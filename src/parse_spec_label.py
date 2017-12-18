#!/home/ww8/anaconda3/bin/python3.6

from bs4 import BeautifulSoup
import lxml
import os, sys

# created by Zeyu Li zyli@cs.ucla.edu
# extract only specific sections inluding "Abstract" and "Introduction" from the xml_data

TAG_LIST = set(['introduction',
                'conclusion',
                'discussion',
                'application',
                'description'
                ])
INVALID_TAG = [
            'listbibl',
            'biblstruct',
            'sourceDesc',
            'filedesc',
            'formula',
            'encodingdesc',
            'ref',
            'figure',
            'back'
            ]

def extract(raw_text):
    soup = BeautifulSoup(raw_text, "xml")
    for tag in soup.find_all(True):
        if tag.name in INVALID_TAG:
            tag.extract()
    text_list = []

    try:
        abstract_txt = str(soup.find("abstract").text)
        text_list.append(abstract_txt.strip())

        # Find all the div's
        divs = soup.find_all(["div", "note"])
        for div in divs:
            if 'type' not in div.attrs:
                if div.find(["head"]).text.lower() in TAG_LIST:
                    # print(div.find(["head"]))
                    div_text = div.text.encode("ascii", errors="ignore").decode()
                    text_list.append(div_text.strip())
    except:
        pass

    return text_list

if __name__ == "__main__":
    DATA_DIR = "../data/"
    INPUT_DIR = DATA_DIR + "xml_data/"
    RESULT_DIR = "../data/"
    OUTPUT_DIR = RESULT_DIR + "parsed_label_text/"
    files = os.listdir(INPUT_DIR)
    total = len(files)
    idx = 0
    for f in files:
        idx += 1
        if idx % 200 == 0:
            print("idx / total = {}".format(idx/total))
        fout_name = f.strip()
        fout_name = os.path.splitext(os.path.basename(fout_name))[0]
        with open(INPUT_DIR + f, "r") as fin, \
            open(OUTPUT_DIR + fout_name + ".txt", "w") as fout:
            doc = fin.read()
            parsed_doc = "\n".join(extract(doc))
            # print(parsed_doc)
            fout.write(parsed_doc)
