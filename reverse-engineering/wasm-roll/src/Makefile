CC=emcc
OUTPUT_FOLDER=./build

build:
	mkdir $(OUTPUT_FOLDER)
	$(CC) ./main.c  -s WASM=1 -o $(OUTPUT_FOLDER)/index.html --shell-file ./index.html -s NO_EXIT_RUNTIME=1 -s LINKABLE=1 -s EXPORTED_RUNTIME_METHODS='["ccall","UTF8ToString"]'
clean:
	rm -rf $(OUTPUT_FOLDER)

