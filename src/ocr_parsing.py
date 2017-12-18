#!/home/ww8/anaconda3/bin/python

import subprocess
import os, sys, shutil
import multiprocessing as mp

# created by Zeyu Li zyli@cs.ucla.edu, modified by Duan Li dxl360@cs.ucla.edu

# parse pdf files using TesseractOCR in multiple processing
# update the command line parameters to fix the empty parsed output issues

DATA_DIR = "./data/"
PDF_DIR = DATA_DIR + "pdfDir/"
TMP_DIR = DATA_DIR + "pdf2tiff/"
OUT_DIR = DATA_DIR + "ocr_parsed_pdf/"

def func(file):
    print("Working on {} ".format(file))
    bn_file = os.path.splitext(file)[0]
    cmd_convert = ['convert', '-density', '500',
                   PDF_DIR + file,
                   '-depth', '8', '-colorspace', 'GRAY', '-alpha', 'Off',
                   TMP_DIR + bn_file + '.tiff']
    cmd_ocr = ['tesseract',
               TMP_DIR + bn_file + '.tiff',
               OUT_DIR + bn_file ]
    subprocess.call(cmd_convert)
    subprocess.call(cmd_ocr)


if __name__ == "__main__":

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    else:
        shutil.rmtree(TMP_DIR)

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    else:
        shutil.rmtree(OUT_DIR)

    file_names = os.listdir(PDF_DIR)
    total = len(file_names)

    # Do multiprocessing works

    pool = mp.Pool(processes=6)
    for file in file_names:
        pool.apply_async(func=func, args=(file, ))
    pool.close()
    pool.join()

