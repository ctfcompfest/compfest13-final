# Writeup WASMROLL

2 ways:
* Reverse .wasm file using `wasm-decompile`, find and reverse `print_flag` and decrypt `int flag[]`
* Roll until you get flag address, analyze memory using js `Module`