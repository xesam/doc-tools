import os

import pikepdf
from PyPDF2 import PdfFileReader, PdfFileWriter


def _extract(in_pdf_file, *pages):
    """抽取指定页"""
    output = PdfFileWriter()
    for page_index in pages:
        output.addPage(in_pdf_file.getPage(page_index))
    return output


def _extract_to_file(in_pdf_path, out_pdf_path, *pages):
    with open(in_pdf_path, 'rb') as in_pdf:
        pdf_file = PdfFileReader(in_pdf)
        with open(out_pdf_path, 'ab') as out_pdf:
            output = _extract(pdf_file, *pages)
            output.write(out_pdf)


def pdf_split_old(pdf_in, pdf_out, start, end):
    pass
    output = PdfFileWriter()
    with open(pdf_in, 'rb') as in_pdf:
        pdf_file = PdfFileReader(in_pdf)
        for i in range(start, end):
            output.addPage(pdf_file.getPage(i))
        with open(pdf_out, 'ab') as out_pdf:
            output.write(out_pdf)


def pdf_split(pdf_in_path, pdf_out_path, start, end):
    pass
    output = PdfFileWriter()
    with open(pdf_in_path, 'rb') as in_pdf:
        pdf_file = PdfFileReader(in_pdf)
        page_end = end if end != -1 else pdf_file.numPages
        for i in range(start, page_end):
            output.addPage(pdf_file.getPage(i))
        with open(pdf_out_path, 'ab') as out_pdf:
            output.write(out_pdf)


def pdf_split2(pdf_in, pdf_out, start, end):
    output = PdfFileWriter()
    pdf_file = PdfFileReader(pdf_in)  # todo 这里不用重复创建
    for i in range(start, end):
        output.addPage(pdf_file.getPage(i))
    output.write(pdf_out)


def split(pdf_in_path, pdf_out_path, splits):
    with open(pdf_in_path, 'rb') as in_pdf:
        with open(pdf_out_path, 'ab') as out_pdf:
            for start, end in splits:
                pdf_split(in_pdf, out_pdf, start, end)


def split_with_starts(pdf_in_path, *starts, **kwargs):
    pass


def add_suffix(file_path, suffix):
    fgs = list(os.path.splitext(file_path))
    fgs[-1:] = ['-', suffix, fgs[-1]]
    return "".join(fgs)


def create_unlock(in_file_path):
    out_file_path = add_suffix(in_file_path, 'unlock')
    with pikepdf.open(in_file_path) as pdf:
        pdf.save(out_file_path)
    return out_file_path


def create_splits(*starts):
    ends = list(starts[1:]) + [-1]
    return zip(starts, ends)


def pages_to_indexes(*pages):
    return [x - 1 for x in pages]


if __name__ == '__main__':
    pass
    # test_pdf_path_1 = "C:/Users/xe/Desktop/1-4/22-轻1-注会-税法【1-4章】-unlock.pdf"
    test_pdf_path_1 = "C:/Users/xe/Desktop/pdfs/注会财管-公式大全.pdf"
    starts = [1, 25, 64, 210, 279]
    indexes = pages_to_indexes(*starts)
    test_splits = list(create_splits(*indexes))
    reader = PdfFileReader(test_pdf_path_1)
    if reader.isEncrypted:
        create_unlock(test_pdf_path_1)
    for index, (start, end) in enumerate(test_splits):
        print(index, start, end)
        pdf_split(
            test_pdf_path_1,
            f"C:/Users/xe/Desktop/1-4/22-轻1-注会-税法【1-4章】-{index}.pdf",
            start,
            end)
