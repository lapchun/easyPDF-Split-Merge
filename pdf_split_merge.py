import re
from collections import OrderedDict
from typing import List
import PyPDF2

# Interpret the page numbers in the config.txt
def interpret_page_numbers(page_numbers: str) -> List[int]:
    numbers = []
# Delete the blank space，use the comma to split the page numbers and construct a list
    page_numbers_list = page_numbers.replace(" ", "").split(",")
# Without page numbers, it will raise a error(but it doesn't work well!!!)
    if len(page_numbers_list) == 0:
        raise ValueError("There are no page numbers determined.")
# Deal with the page numbers with "-"
    for p in page_numbers_list:
        if len(re.findall(r"-", p)) == 1:
            start_n, end_n = p.split("-")
            start_n = int(start_n)
            end_n = int(end_n)
            numbers.extend(list(range(start_n, end_n + 1)))
        else:
            numbers.append(int(p))
# Remove duplication, construct a list, sort
    return sorted(list(set(numbers)))

# Interpret the config.txt
def interpret_config_file(file_path: str, file_encoding: str = None) -> dict:
    with open(file_path, "r", encoding=file_encoding) as f:
        lines = f.readlines()

# A special dictionary that sorts all items by the appending order
    d = OrderedDict()
# Construct index sequence, including data index and data
    for i, line in enumerate(lines, start=1):
        l = line.split(".pdf")

        if len(l) != 2:
            raise ValueError("Something is wrong with the config file at line: {0} -> {1}".format(i, line))

        pdf_file_path = l[0] + ".pdf"
        page_numbers = interpret_page_numbers(l[1])

        d[i] = {pdf_file_path: page_numbers}

    return d

# Extract the content of interesting pages according the dictionary
def extract_interesting_pdf_pages(pdf_dict: dict) -> list:
    pages = []

    for pdf_file_number, details_dict in pdf_dict.items():
        pdf_file_path = list(details_dict.keys())[0]
        page_numbers = list(details_dict.values())[0]

        pdf = PyPDF2.PdfFileReader(pdf_file_path)
        for i in page_numbers:
            p = i - 1
            try:
                pages.append(pdf.getPage(p))
            except:
                print("There is no page: {0} in pdf file: {1}, so it is skipped.".format(i, pdf_file_path))
    return pages

# Merge the content of interesting pages
def merge_pdf_pages(pdf_pages: list) -> PyPDF2.PdfFileWriter:
    pdf = PyPDF2.PdfFileWriter()
    for p in pdf_pages:
        pdf.addPage(p)
    return pdf

# Split and merge the PDF files according to the input and output
def split_and_merge(input: str, output: str):
    input_config_file_path = input
    output_pdf_file_path = output
    file_encoding = None

    pdf_dict = interpret_config_file(input_config_file_path, file_encoding)
    interesting_pdf_pages = extract_interesting_pdf_pages(pdf_dict)
    pdf = merge_pdf_pages(interesting_pdf_pages)

    with open(output_pdf_file_path, "wb") as f:
        pdf.write(f)

    print("[*] Final number of pages in the new document: {0}".format(pdf.getNumPages()))
    print("[*] Split and Merge is done! File is written to path: {0}".format(output_pdf_file_path))

if __name__ == '__main__':
    split_and_merge("config.txt", "new.pdf")
    print("Finish!")
