import os

import pikepdf
from PyPDF2 import PdfFileReader, PdfFileWriter


def _extract_range(in_pdf, page_range):
    """抽取指定页"""
    pages = []
    for page_index in range(*page_range):
        pages.append(in_pdf.getPage(page_index))
    return pages


def _extract_range_to_pdf(in_pdf, out_pdf, page_range):
    """抽取指定页并添加到 out_file 的尾部"""
    pages = _extract_range(in_pdf, page_range)
    for page in pages:
        out_pdf.addPage(page)
    return out_pdf


def _extract_ranges_to_pdf(in_pdf, out_pdf, *page_ranges):
    """抽取指定页并添加到 out_file 的尾部"""
    for page_range in page_ranges:
        _extract_range_to_pdf(in_pdf, out_pdf, page_range)


def add_suffix(file_path, suffix):
    fgs = list(os.path.splitext(file_path))
    fgs[-1:] = ['-', suffix, fgs[-1]]
    return "".join(fgs)


def create_unlock(in_file_path, out_unlock_file_path):
    with pikepdf.open(in_file_path) as pdf:
        pdf.save(out_unlock_file_path)
    return out_unlock_file_path


def prepare_unlock(in_file_path):
    reader = PdfFileReader(in_file_path)
    if reader.isEncrypted:
        out_file_path = add_suffix(in_file_path, 'unlock')
        return create_unlock(in_file_path, out_file_path)
    else:
        return in_file_path


def _extract_to_merged_pdf(in_pdf_file_path, out_pdf_file_path, page_ranges):
    """抽取到一个合并的文件中"""
    with open(in_pdf_file_path, 'rb') as in_pdf_file:
        in_pdf = PdfFileReader(in_pdf_file)
        with open(out_pdf_file_path, 'ab') as out_pdf_file:
            out_pdf = PdfFileWriter()
            _extract_ranges_to_pdf(in_pdf, out_pdf, [1, 2], [3, 4])
            out_pdf.write(out_pdf_file)


def _extract_to_diff_pdf(in_pdf_file_path, page_ranges):
    """抽取到一个各自的文件中"""
    with open(in_pdf_file_path, 'rb') as in_pdf_file:
        in_pdf = PdfFileReader(in_pdf_file)
        for page_range in page_ranges:
            out_pdf_file_path = add_suffix(in_pdf_file_path, f'{page_range[0]}-{page_range[1]}')
            with open(out_pdf_file_path, 'ab') as out_pdf_file:
                out_pdf = PdfFileWriter()
                _extract_range_to_pdf(in_pdf, out_pdf, page_range)
                out_pdf.write(out_pdf_file)


def t():
    test_in_pdf_file_path = "./1.pdf"
    page_ranges = [[1, 2], [3, 4]]
    _extract_to_merged_pdf(test_in_pdf_file_path, add_suffix(test_in_pdf_file_path, 'out'), page_ranges)


if __name__ == '__main__':
    pass
    t()
