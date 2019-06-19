if has('python3')
    let s:python = 'python3 << endPython'
    let s:using_python3 = 1
elseif has('python')
    let s:python = 'python << endPython'
    let s:using_python3 = 0
else
    echoerr 'Could not start clangdestine.vim: requires Vim compiled with Python support.'
endif

" setup clangdestine
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
        yaml_path = os.path.join(path, "third_party", "pyyaml", lib_dir)
        sys.path.append(yaml_path)
        break

import clangdestine
endPython
" end setup clangdestine

fun s:UpdateCinoptions()
exe s:python
clangdestine.update_cinoptions()
endPython
endfun

autocmd FileType cpp call s:UpdateCinoptions()
