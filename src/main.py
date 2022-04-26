from PyPDF2 import PdfFileWriter, PdfFileReader


def pdf_split(pdf_in, pdf_out, start, end):
    pass
    output = PdfFileWriter()
    with open(pdf_in, 'rb') as in_pdf:
        pdf_file = PdfFileReader(in_pdf)
        for i in range(start, end):
            output.addPage(pdf_file.getPage(i))
        with open(pdf_out, 'ab') as out_pdf:
            output.write(out_pdf)


if __name__ == '__main__':
    pass
