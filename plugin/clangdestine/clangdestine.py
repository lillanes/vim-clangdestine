from os import path
import vim
import yaml

def find_clang_format_file(start_directory):
    f = path.join(start_directory, ".clang-format")
    if path.exists(f) and path.isfile(f):
        return f
    parent = path.dirname(start_directory)
    if path.basename(parent):
        return find_clang_format_file(parent)
    return None


def set_clang_format_file(start_directory):
    f = find_clang_format_file(start_directory)
    if f is not None:
        vim.command("let b:clang_format_file='%s'" % f)
