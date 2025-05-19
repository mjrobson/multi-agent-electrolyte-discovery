"""
PDF Text Extraction Utilities
Author: Matt Robson
Date: 12.5.2025
"""

import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


def extract_text_from_pdf(pdf_path: str, output_folder: str) -> None:
    """
    Extracts all text from a PDF and saves it to a .txt file.

    Args:
        pdf_path: Path to the input PDF file.
        output_folder: Directory to save the extracted text file.
    """
    os.makedirs(output_folder, exist_ok=True)

    base_name = os.path.basename(pdf_path)
    output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}.txt")

    text_blocks = []
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text_blocks.append(element.get_text().strip())

    with open(output_file, "w") as f:
        f.write(" ".join(text_blocks))


def clean_line_breaks(file_path: str) -> None:
    """
    Normalizes text by removing newline characters from a file.

    Args:
        file_path: Path to the .txt file to clean.
    """
    with open(file_path, "r+") as f:
        content = f.read()
        f.seek(0)
        f.write(content.replace("\n", " "))
        f.truncate()


def process_pdf_batch(pdf_dir: str, output_dir: str) -> None:
    """
    Processes all PDFs in a directory: extracts text and cleans line breaks.

    Args:
        pdf_dir: Directory containing PDF files.
        output_dir: Directory where processed .txt files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith(".pdf")]
    print(f"Found {len(pdf_files)} PDF file(s) to process")

    for pdf_file in pdf_files:
        extract_text_from_pdf(
            os.path.join(pdf_dir, pdf_file),
            output_dir
        )
        print(f"Processed: {pdf_file}")

    txt_files = [f for f in os.listdir(output_dir) if f.endswith(".txt")]
    print(f"Cleaning {len(txt_files)} text file(s)")

    for txt_file in txt_files:
        clean_line_breaks(os.path.join(output_dir, txt_file))

    print(f"✅ Processing complete! Results saved to: {output_dir}")

