set tabstop=4
set shiftwidth=4
set smarttab
set expandtab
set softtabstop=4
set autoindent
set fileencodings=utf-8,latin1,latin2
syn on

set list listchars=tab:»·,trail:·

au FileType make setlocal noexpandtab

" Fixing Cut/Copy/Paste on Gtk Vim on Ubuntu 12.04
vmap <C-c> "+yi
vmap <C-x> "+c
vmap <C-v> c<ESC>"+p
imap <C-v> <ESC>"+pa

