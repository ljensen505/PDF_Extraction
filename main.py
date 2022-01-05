"""
Written by Lucas Jensen for White Bird Clinic
Last updated 12/29/2021
Extracts individual PDFs from a large PDF file and names them according to a corresponding csv file
"""

import PyPDF2
import csv
import os

pdf_file = "November clinics/11.8.pdf"
csv_file = "November clinics/11-8-21.csv"
clinic_date = "11-8"


def make_name_list(names):
    """
    opens a csv file and generates a list of names from it
    :param names: a csv file containing patient names
    :return: a list containing those names
    """
    with open(names, 'r') as infile:
        names = []
        reader = csv.reader(infile)
        for name in reader:
            names.append(name)

    return names[0]


def make_pdfs(in_pdf, names):
    """
    creates a pdf for each patient
    :param in_pdf: a single pdf file containing pages to extract
    :param names: a list of patient names
    :return: nothing
    """
    inputpdf = PyPDF2.PdfFileReader(open(in_pdf, "rb"))
    os.mkdir(f"extracted/extracted{clinic_date}")

    for i in range(len(names)):
        name = names[i]
        output = PyPDF2.PdfFileWriter()
        output.addPage(inputpdf.getPage(i * 2))
        output.addPage(inputpdf.getPage((i * 2) + 1))
        with open(f"extracted/extracted{clinic_date}/Scanned_Consent-{name}-{clinic_date}.pdf", "wb") as outputStream:
            output.write(outputStream)


def is_count_match(names, in_pdf):
    """
    determines of the list of names is the correct length for the number of PDF pages
    :param names: a list of names, previously generated from a csv file
    :param in_pdf: the pdf of consent forms
    :return: bool
    """
    pdf = PyPDF2.PdfFileReader(open(in_pdf, 'rb'))
    pdf_count = pdf.getNumPages()
    pdf_count /= 2
    if len(names) == pdf_count:
        return True
    return False


def main():
    """
    the main function for extracting PDFs
    :return: nothing
    """
    names = make_name_list(csv_file)
    if is_count_match(names, pdf_file):
        make_pdfs(pdf_file, names)
    else:
        print("Something went wrong. The CSV and PDF are of different lengths.")


main()
