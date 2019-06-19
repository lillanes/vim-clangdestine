if has('python3')
    let s:python = 'python3 << EOF'
elseif has('python')
    let s:python = 'python << EOF'
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
            break

import clangdestine
EOF
" end setup clangdestine

fun FindAndPrint()
exe s:python
clangdestine.set_clang_format_file(vim.eval("expand('%:p')"))
EOF
endfun

autocmd FileType cpp call FindAndPrint()
