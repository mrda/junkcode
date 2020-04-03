set tabstop=4
set shiftwidth=4
set smarttab
set expandtab
set softtabstop=4
set autoindent
set fileencodings=utf-8,latin1,latin2
syn on

set list listchars=tab:»·,trail:·
set guifont=Monospace\ 14

au FileType make setlocal noexpandtab

" Fixing Cut/Copy/Paste on Gtk Vim on Ubuntu 12.04
"vmap <C-c> "+yi
"vmap <C-x> "+c
"vmap <C-v> c<ESC>"+p
"imap <C-v> <ESC>"+pa
"
nmap <C-c> "+y
imap <C-c> "+y
vmap <C-c> "+y
nmap <C-x> "+x
imap <C-x> "+x
vmap <C-x> "+x
nmap <C-v> "+gP
imap <C-v> "+gP
vmap <C-v> "+gP
imap <D-v> "+gP

" Function key remappings

" <F5> - Insert RCS Date String
nmap <F5> "=strftime("%Y/%m/%d %H:%M:%S")<CR>p
imap <F5> <C-R>=strftime("%Y/%m/%d %H:%M:%S")<CR>



