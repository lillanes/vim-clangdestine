" clangdestine.vim - Automatically set cinoptions from clang-format file
" Maintainer:   León Illanes <https://github.com/lillanes/>
" Version:      0.0.1

if exists("g:loaded_clangdestine")
    finish
endif

command ClangdestineUpdateCinoptions call clangdestine#UpdateCinoptions()
autocmd FileType c,cpp ClangdestineUpdateCinoptions

let g:loaded_clangdestine = 1
