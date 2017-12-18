import os
import re

# created by by Duan Li dxl360@cs.ucla.edu

# fix the missing url issues of xml data files

if __name__ == "__main__":
    DATA_DIR = "../data/"

    INPUT_DIR = DATA_DIR + "ocr_parsed_pdf/"
    INPUT_DIR2 = DATA_DIR + "old/xml_data/"
    OUTPUT_DIR = DATA_DIR + "xml_data/"
    file_list1 = os.listdir(INPUT_DIR)
    file_list2 = os.listdir(INPUT_DIR2)
    idx1, total1 = 0, len(file_list1)
    idx2, total2 = 0, len(file_list2)
    pattern = r'available at'
    text = "available at "
    regex_url_space = r'(\w+\s\w+\s\w+\s\w+\s\w+\s)' \
                        + pattern + r' ' + \
                       r'(\http[s]?://(?:[a-zA-Z]|[0-9]|[\n]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
    regex = r'(\w+\s\w+\s\w+\s\w+\s\w+\s)' \
             + pattern + \
             r'</p>'

#    regex_url_space = r'(\w+\s\w+\s\w+\s\w+\s\w+\s)(\http[s]?://(?:[a-zA-Z]|[0-9]|[\n]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
#    regex = r'(\w+\s\w+\s\w+\s\w+\s\w+\s)http[s]?://</p>'
    # regex = r'(\w+\s\w+\s\w+\s)available at</p>'
    temp = []
    count = 0
    for f1 in file_list1:
        idx1 += 1
        if idx1 % 300 == 0:
            print(idx1 / total1)
        with open(INPUT_DIR + f1, "r", errors='replace') as fin1:
            fin_paras1 = fin1.readlines()
            for i in range(len(fin_paras1)):
                urls = re.search(regex_url_space, fin_paras1[i])
                if urls != None:
                    fin_paras1[i] = fin_paras1[i].rstrip() + fin_paras1[i + 1].rstrip()
            for para in fin_paras1:
                urls = re.findall(regex_url_space, para)
                for url in urls:
                    temp.append(url)
                    # print(url)

    for f2 in file_list2:
        idx2 += 1
        if idx2 % 300 == 0:
            print(idx2 / total2)
        with open(INPUT_DIR2 + f2, "r") as fin2:
            with open(OUTPUT_DIR + f2, "w") as fout:
                fin_paras2 = fin2.readlines()
                for paras2 in fin_paras2:
                    flag = 0
                    missed_urls = re.findall(regex, paras2)
                    for missed in missed_urls:
                        # print (missed)
                        for tmp in temp:
                            if (missed == tmp[0]):
                                count += 1
                                # print(paras2)
                                paras2 = re.sub(regex, tmp[0] + text + tmp[1], paras2)
                                # paras2 = re.sub(regex, tmp[0] + tmp[1], paras2)
                                if (flag == 0):
                                    print(paras2)
                                    fout.write(paras2)
                                    flag = 1
                                continue
                    if (flag == 0):
                        fout.write(paras2)
    print(count)
