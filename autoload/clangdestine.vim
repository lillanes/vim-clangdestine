" clangdestine.vim - Automatically set cinoptions from clang-format file
" Maintainer:   León Illanes <https://github.com/lillanes/>
" Version:      0.0.1

if has('python3')
    let s:python = 'python3 << endPython'
    let s:using_python3 = 1
elseif has('python')
    let s:python = 'python << endPython'
    let s:using_python3 = 0
else
    echoerr 'Could not start clangdestine.vim: requires Vim compiled with Python support.'
endif

exe s:python
import os, sys, vim

for path in vim.eval("&runtimepath").split(","):
    plugin_path = os.path.join(path, "plugin")
    if os.path.exists(os.path.join(plugin_path, "clangdestine")):
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)

        if int(vim.eval("s:using_python3")):
            lib_dir = "lib3"
        else:
            lib_dir = "lib"
        libyaml_path = os.path.join(path, "third_party", "pyyaml", lib_dir)
        sys.path.append(libyaml_path)
        break

import clangdestine
endPython

if !exists("g:clangdestine_format_file")
    let g:clangdestine_format_file = ""
endif

fun clangdestine#UpdateCinoptions()
exe s:python
clangdestine.update_cinoptions(plugin_path)
endPython
endfun
