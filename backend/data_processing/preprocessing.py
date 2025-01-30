# TODO: 1. create a general purpose chunking code using unstructured library
# TODO 2. create  it in such a way that anyone can use it directly by
# plugging in the folder of documents and create chunks
# also figure out if we can make a general pipeline to create embeddings
# from the chunks obtained from the folder.

import json
import os

import pandas as pd
from tqdm import tqdm
from unstructured.partition.pdf import partition_pdf


def extract_chunks_from_pdfs(folder_path, output_folder="processed_chunks2"):
    """
    Extracts chunks from all PDFs in the folder, saves them as JSON files, and preserves `orig_elements`.

    Args:
        folder_path (str): Path to the folder containing PDF files.
        output_folder (str): Path to save processed chunks.
    """
    os.makedirs(output_folder, exist_ok=True)
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    for file in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
        output_file = os.path.join(output_folder, f"{file}.json")

        # Skip processing if the file is already saved
        if os.path.exists(output_file):
            print(f"Skipping {file}, already processed.")
            continue

        file_path = os.path.join(folder_path, file)
        chunks = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="hi_res",
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
        )

        # Convert chunks to JSON serializable format
        chunk_data = []
        for chunk in chunks:
            chunk_dict = chunk.to_dict()

            # Preserve original elements if available
            if (
                hasattr(chunk.metadata, "orig_elements")
                and chunk.metadata.orig_elements
            ):
                chunk_dict["metadata"]["orig_elements"] = [
                    elem.to_dict() for elem in chunk.metadata.orig_elements
                ]

            chunk_data.append(chunk_dict)

        # Save to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=4)

        print(f"Processed and saved {file}.")


all_chunks = extract_chunks_from_pdfs("../../policy_documents")
