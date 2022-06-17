import os


def add_suffix_to_basename(file_path, suffix):
    fgs = list(os.path.splitext(file_path))
    fgs[-1:] = ['-', suffix, fgs[-1]]
    return "".join(fgs)
