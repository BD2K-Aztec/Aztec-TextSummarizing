#!/home/ww8/anaconda3/bin/python3.6

# created by Zeyu Li (zyli@cs.ucla.edu)

# From xml to plan text
#   - Remove some tags
#   - Keep certain tags and write to `./data/parsed_text/`

from bs4 import BeautifulSoup
import sys
import os


def extract_text(raw_text):
    soup = BeautifulSoup(raw_text, 'lxml')
    # Remove all the invalid tags that won't appear in parsed text.
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

    for tag in soup.find_all(True):
        if tag.name in INVALID_TAG:
            tag.extract()

    text_list = []
    # After remove all the invalid tag, deal with the abstract
    try:
        abstract_txt = str(soup.find("abstract").text)
        text_list.append(abstract_txt.strip())
        # Deal with each div
        divs = soup.find_all(["div", "note"])
        for each_div in divs:
            if 'type' not in each_div.attrs:
                div_text = each_div.text.encode("ascii", errors="ignore").decode()
                text_list.append(div_text.strip())
    except:
        pass
    return text_list

if __name__ == "__main__":
    DATA_DIR = "./data/"
    RAW_DIR = DATA_DIR + "xml_data/"
    PARSED_DIR = DATA_DIR + "parsed_text/"
    file_list = os.listdir(RAW_DIR)

    # Read the files
    idx, total = 0, len(file_list)
    for file_name in file_list:
        idx += 1
        file_name = file_name.strip()
        file_name_noext = os.path.splitext(os.path.basename(file_name))[0]
        if idx % 300 == 0:
            print("{}% finished".format(int(idx / total * 100)))
        with open(RAW_DIR + file_name, "r") as file_in:
            with open(PARSED_DIR + file_name_noext + ".txt", "w") as file_out:
                raw_text = file_in.read()
                for paragraph in extract_text(raw_text):
                    file_out.write(paragraph + "\n")

