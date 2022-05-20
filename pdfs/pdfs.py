import os

import pikepdf
from PyPDF2 import PdfFileReader, PdfFileWriter


def _extract_range(in_pdf, page_collection):
    """抽取指定页"""
    return [in_pdf.getPage(pagination - 1) for pagination in page_collection]


def _extract_range_to_pdf(in_pdf, out_pdf, page_collection):
    """抽取指定页并添加到 out_pdf 的尾部"""
    pdfPages = _extract_range(in_pdf, page_collection)
    for pdfPage in pdfPages:
        out_pdf.addPage(pdfPage)
    return out_pdf


def _extract_ranges_to_pdf(in_pdf, out_pdf, *page_collections):
    """抽取指定页并添加到 out_pdf 的尾部"""
    for page_range in page_collections:
        _extract_range_to_pdf(in_pdf, out_pdf, page_range)


def add_suffix_to_basename(file_path, suffix):
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
        out_file_path = add_suffix_to_basename(in_file_path, 'unlock')
        return create_unlock(in_file_path, out_file_path)
    else:
        return in_file_path


def extract_to_merged_pdf(in_pdf_file_path, out_pdf_file_path, *page_collections):
    """抽取到一个合并的文件中"""
    with open(in_pdf_file_path, 'rb') as in_pdf_file:
        in_pdf = PdfFileReader(in_pdf_file)
        with open(out_pdf_file_path, 'ab') as out_pdf_file:
            out_pdf = PdfFileWriter()
            _extract_ranges_to_pdf(in_pdf, out_pdf, *page_collections)
            out_pdf.write(out_pdf_file)


def extract_to_diff_pdf(in_pdf_file_path, out_pdf_dir, *page_collections):
    """抽取到一个各自的文件中"""
    with open(in_pdf_file_path, 'rb') as in_pdf_file:
        in_pdf = PdfFileReader(in_pdf_file)
        for page_collection in page_collections:
            input_basename = os.path.basename(in_pdf_file_path)
            output_basename = add_suffix_to_basename(input_basename, page_collection.get_collection_name())
            out_pdf_file_path = os.path.join(out_pdf_dir, output_basename)
            with open(out_pdf_file_path, 'ab') as out_pdf_file:
                out_pdf = PdfFileWriter()
                _extract_range_to_pdf(in_pdf, out_pdf, page_collection)
                out_pdf.write(out_pdf_file)
