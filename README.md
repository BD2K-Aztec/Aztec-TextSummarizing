# Aztec-TextSummarizing

Data files:

data/ocr_parsed_pdf: the output of TesseractOCR given original pdf as input

data/parsed_label_text: extracting only "Abstract" and "Introduction" from the xml_data

data/parsed_text: from xml_data, remove all noise terms including references, figure captions, tables, etc, and remove all xml tags

data/parsed_seg_text: from parsed_text, parsed through worksegmentation packages in python to transform "introductionthis is" to "introduction this is"

data/xml_data: the output of Grobid given original pdf as input

data/pdfDir: original pdf files

data/pdf2tiff: intermediate files produced when using TessaractOCR to parse the pdf files, file size is too large to commit, please download at

data/old: original parsed_label_text and xml_data



Source code files: 

src/keypar.py: keyword-based sentence extraction

src/ocr_parsing: TesseractOCR parsing in multiple processing

src/parse.py: generate the data/parsed_text

src/parse_spec_label.py: generate the data/parsed_label_text

src/wordseg.py: do the word segmentation

src/fix_missing_url.py: merge the text from ocr_parsed_pdf and xml_data to fix the missing url issue

src/create_test_file.py: create test file for model training

src/train_model.py: train the model based on 100 manually labeled documents

src/train_model_2.py: update the training model 



Reference files:

ref/software_vocab.txt: software relevant keywords, input file of keypar.py

ref/stopwords.txt: stop words/software non-relevant keywords, input file of train_model_2.py



Output files:

result/output_1.csv: predicted result of the documents based on training file

result/output_2.csv: updated predicted resulf of documents based on training file

result/train.csv: training file with extracted sentence and label

result/labeled1_100: manually labeled 100 documents, treated as training data
