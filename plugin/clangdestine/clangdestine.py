from __future__ import print_function
from os import path
import vim
import yaml

def find_clang_format_file(directory):
    f = path.join(directory, ".clang-format")
    if path.exists(f) and path.isfile(f):
        return f
    parent = path.dirname(directory)
    if path.basename(parent):
        return find_clang_format_file(parent)
    return None


def get_clang_format_file():
    try:
        f = vim.eval("b:clang_format_file")
    except:
        directory = vim.eval("expand('%:p')")
        f = find_clang_format_file(directory)
    return f


def get_format():
    format_filename = get_clang_format_file()
    with open(format_filename) as format_file:
        return yaml.load(format_file, Loader=yaml.Loader)


FALLBACK_STYLE = 'LLVM'
def get_defaults(named_style):
    # FIXME should do this and not return something fixed:
    # if named_style is None:
    #     named_style = FALLBACK_STYLE
    # with open("%s.yaml" % named_style) as style:
    #     return yaml.load(style, Loader=yaml.loader)
    return {'AccessModifierOffset': 0,
            'AlignAfterOpenBracket': True,
            'ContinuationIndentWidth': 4,
            'ConstructorInitializerIndentWidth': 4,
            'IndentCaseLabels': False,
            'IndentWidth': 2,
            'NamespaceIndentation': 'None',
            }


def get_value_or_default(item, format_data, default_values):
    if item in format_data:
        return format_data[item]
    return default_values[item]


def access_modifier_offset(format_data, default_values):
    offset = get_value_or_default('AccessModifierOffset', format_data,
            default_values)
    indent = get_value_or_default('IndentWidth', format_data, default_values)

    vim_offset = offset + indent
    return "g%d" % vim_offset


def align_after_open_bracket(format_data, default_values):
    value = get_value_or_default('AlignAfterOpenBracket', format_data,
            default_values)
    if value:
        return "(0"

    indent = get_value_or_default('ContinuationIndentWidth', format_data,
            default_values)
    return "(%d" % indent


def construction_initializer_indent_width(format_data, default_values):
    value = get_value_or_default('ConstructorInitializerIndentWidth',
            format_data, default_values)
    return "i%d" % value


def continuation_indent_width(format_data, default_values):
    value = get_value_or_default('ContinuationIndentWidth', format_data,
            default_values)
    return "+%d" % value


def indent_case_labels(format_data, default_values):
    value = get_value_or_default('IndentCaseLabels', format_data,
            default_values)
    if value:
        indent = get_value_or_default('IndentWidth', format_data,
                default_values)
        return ":%d,l1" % indent
    return ":0,l1"


def indent_width(format_data, default_values):
    value = get_value_or_default('IndentWidth', format_data, default_values)
    return ">%d" % value


def namespace_indentation(format_data, default_values):
    value = get_value_or_default('NamespaceIndentation', format_data,
            default_values)

    if value == "None":
        indent = get_value_or_default('IndentWidth', format_data,
                default_values)
        return "N-%d" % indent
    elif value == "Inner":
        pass
    elif value == "All":
        pass
    else:
        assert False, ("NamespaceIndentation value of '%s' is unrecognized "
                       "(should be 'None', 'Inner', or 'All').") % value


def update_cinoptions():
    format_data = get_format()

    if 'BasedOnStyle' in format_data:
        default_values = get_defaults(format_data['BasedOnStyle'])
    else:
        default_values = get_defaults(None)

    translations = [
            access_modifier_offset,
            align_after_open_bracket,
            construction_initializer_indent_width,
            continuation_indent_width,
            indent_case_labels,
            indent_width,
            namespace_indentation,
            ]

    cinoptions = [f(format_data, default_values) for f in translations]
    cinoptions = ",".join(cinoptions)

    vim.command("set cinoptions=%s" % cinoptions)
