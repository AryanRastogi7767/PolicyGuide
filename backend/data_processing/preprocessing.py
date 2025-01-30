# TODO: 1. create a general purpose chunking code using unstructured library
# TODO 2. create  it in such a way that anyone can use it directly by
# plugging in the folder of documents and create chunks
# also figure out if we can make a general pipeline to create embeddings
# from the chunks obtained from the folder.

import os

from unstructured.partition.pdf import partition_pdf

PDF_FOLDER = "../../policy_documents/"
PDF_LIST = os.listdir(PDF_FOLDER)
print(PDF_LIST)
