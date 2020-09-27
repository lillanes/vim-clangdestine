from __future__ import print_function
from os import path
import vim
import yaml


def find_clang_format_file(directory=None):
    if directory is None:
        directory = vim.eval("expand('%:p')")
    f = path.join(directory, ".clang-format")
    if path.exists(f) and path.isfile(f):
        return f
    parent = path.dirname(directory)
    if path.basename(parent):
        return find_clang_format_file(parent)
    return None


def get_vim_variable(variable_name):
    exists = vim.eval("exists('%s')" % variable_name)
    if int(exists):
        value = vim.eval(variable_name)
        return value


def get_global_defined_format_file():
    return get_vim_variable("g:clangdestine_format_file")


def get_buffer_defined_format_file():
    return get_vim_variable("b:clangdestine_format_file")


def get_clang_format_file():
    b = get_buffer_defined_format_file()
    if b:
        return b

    g = get_global_defined_format_file()
    if g:
        return g

    return find_clang_format_file()


def get_format():
    format_filename = get_clang_format_file()
    if format_filename is None:
        return None
    with open(format_filename) as format_file:
        return yaml.load(format_file, Loader=yaml.Loader)


FALLBACK_STYLE = 'LLVM'
def get_defaults(named_style, plugin_path):
    if named_style is None:
        named_style = FALLBACK_STYLE
    style_filename = path.join(plugin_path, "clangdestine", "resources",
            "%s.yaml" % named_style)
    with open(style_filename) as style_file:
        return yaml.load(style_file, Loader=yaml.Loader)


def get_value_or_default(item, format_data, default_values):
    if item in format_data:
        return format_data[item]
    return default_values[item]


def access_modifier_offset(format_data, default_values):
    offset = get_value_or_default('AccessModifierOffset', format_data,
            default_values)
    indent = get_value_or_default('IndentWidth', format_data, default_values)

    vim_offset = int(offset) + int(indent)
    return "g%d" % vim_offset


def align_after_open_bracket(format_data, default_values):
    value = get_value_or_default('AlignAfterOpenBracket', format_data,
            default_values)
    if value == "Align":
        return "(0"
    elif value == "DontAlign" or value == "AlwaysBreak":
        indent = get_value_or_default('ContinuationIndentWidth', format_data,
                default_values)
        return "(%d" % int(indent)
    else:
        assert False, ("AlignAfterOpenBracket value of '%s' is unrecognized "
                       "(should be 'Align', 'DontAlign', or "
                       "'AlwaysBreak').") % value


def break_before_braces(format_data, default_values):
    value = get_value_or_default('BreakBeforeBraces', format_data,
            default_values)

    if value in ["Attach", "Linux", "Mozilla", "Stroustrup", "Allman",
            "WebKit"]:
        return None
    elif value == "GNU":
        # Can't actually do this one, as brace indentation is different for
        # classes or functions vs control blocks.
        return None
    elif value == "Custom":
        braces = get_value_or_default('BraceWrapping', format_data,
                default_values)
        if braces['IndentBraces']:
            indent = get_value_or_default('IndentWidth', format_data,
                    default_values)
            indent = int(indent)
            return "f%d,{%d" % (indent, indent)
        return None
    else:
        assert False, ("BreakBeforeBraces value of '%s' is unrecognized "
                "(should be 'Attach', 'Linux', 'Mozilla', 'Stroustrup', "
                "'Allman', 'WebKit', 'GNU', or 'Custom')") % value


def construction_initializer_indent_width(format_data, default_values):
    value = get_value_or_default('ConstructorInitializerIndentWidth',
            format_data, default_values)
    return "i%d" % int(value)


def continuation_indent_width(format_data, default_values):
    value = get_value_or_default('ContinuationIndentWidth', format_data,
            default_values)
    return "+%d" % int(value)


def indent_case_labels(format_data, default_values):
    value = get_value_or_default('IndentCaseLabels', format_data,
            default_values)
    if value:
        indent = get_value_or_default('IndentWidth', format_data,
                default_values)
        return ":%d,l1" % int(indent)
    return ":0,l1"


def indent_width(format_data, default_values):
    value = get_value_or_default('IndentWidth', format_data, default_values)
    return ">%d" % int(value)


def namespace_indentation(format_data, default_values):
    value = get_value_or_default('NamespaceIndentation', format_data,
            default_values)

    if value == "None":
        indent = get_value_or_default('IndentWidth', format_data,
                default_values)
        return "N-%d" % int(indent)
    elif value == "Inner":
        pass
    elif value == "All":
        pass
    else:
        assert False, ("NamespaceIndentation value of '%s' is unrecognized "
                       "(should be 'None', 'Inner', or 'All').") % value


def disabled():
    flag = get_vim_variable("g:clangdestine_disabled") \
            or get_vim_variable("b:clangdestine_disabled")
    return flag


def update_cinoptions(plugin_path):
    if disabled():
        return

    format_data = get_format()

    if format_data is None:
        return

    if 'BasedOnStyle' in format_data:
        default_values = get_defaults(format_data['BasedOnStyle'], plugin_path)
    else:
        default_values = get_defaults(None, plugin_path)

    translations = [
            access_modifier_offset,
            align_after_open_bracket,
            break_before_braces,
            construction_initializer_indent_width,
            continuation_indent_width,
            indent_case_labels,
            indent_width,
            namespace_indentation,
            ]

    cinoptions = [f(format_data, default_values) for f in translations]
    cinoptions = ",".join([o for o in cinoptions if o is not None])

    vim.command("set cinoptions=%s" % cinoptions)
