#include<stdio.h>
#include<stdlib.h>

int menu() {
    puts("\nMenu:");
    puts("1. Add a book to shelf");
    puts("2. Read a book from shelf");
    puts("3. Rearrange shelf");
    puts("4. Exit");
    printf("> ");
    

    int choice;
	scanf("%d", &choice);
	return choice;
}

void greetings() {
    puts("Keep your books tidy with our bookshelf.");
}

struct book {
    char title[16];
    int page;
};

struct book *bookshelf[8][8];
int bookCountInShelf[8];

void addBook() {
    unsigned int location;

    while (1) {
        printf("Where do you want to put it? (0 - 7): ");
        scanf("%d", &location);
        if (bookCountInShelf[location] < 8) {
            break;
        }
        printf("That row is full, please choose another location.\n");
    }

    bookshelf[location][bookCountInShelf[location]] = malloc(sizeof(struct book));
    struct book *newBook = bookshelf[location][bookCountInShelf[location]];
    bookCountInShelf[location]++;

    printf("Title: ");
    scanf("%16s", newBook->title);
    printf("Page: ");
    scanf("%d", &(newBook->page));
    
    printf("Successfully add %s with %d page(s) to the shelf.\n", newBook->title, newBook->page);
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    for (int i = 0; i < 8; i++) {
        bookCountInShelf[i] = 0;
    }
}

void readBook() {
    unsigned int row, col;
    printf("Which row? (0 - 7): ");
    scanf ("%d", &row);
    printf("Which column? (0 - %d): ", bookCountInShelf[row] - 1);
    scanf("%d", &col);
    if (row > 7 || col > bookCountInShelf[row] - 1) {
        puts("Book not found.");
        return;
    }
    printf("Title: %s\n", bookshelf[row][col]->title);
    printf("Page: %d\n", bookshelf[row][col]->page);
    
    printf("Are you sure you want to read this book? (1/0): ");
    int choice;
    scanf("%d", &choice);
    if (choice == 1) {
        puts("Removing the book from the shelf.");
        free(bookshelf[row][col]);
        bookCountInShelf[row]--;
        for (int j = col; j < bookCountInShelf[row]; j++) {
            bookshelf[row][j] = bookshelf[row][j+1];
        }
    }
}

void rearrange() {
    struct book *tmpBookshelf[64];
    int cnt = 0;

    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < bookCountInShelf[i]; j++) {
            tmpBookshelf[cnt++] = bookshelf[i][j];
        }
    }

    int cntBook = 0;
    for (int i = 0; i < 8; i++) {
        cntBook += bookCountInShelf[i];
        bookCountInShelf[i] = 0;
    }

    cnt = 0;
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
            bookshelf[i][j] = tmpBookshelf[cnt++];
        }
    }
    
    if (cntBook % 8 != 0) {
        for (int i = 0; i < 8; i++) {
            if (cntBook < 8) {
                for (int j = 0; j < cntBook; j++) {
                    printf("Removing %s from shelf because of rearrangement.\n", bookshelf[i][j]->title);
                    free(bookshelf[i][j]);
                }
                break;
            }
            bookCountInShelf[i] = 8;
            cntBook -= 8;
        }
    }
}

int main() {
    init();
    greetings();

    while (1) {
        int choice = menu();
        if (choice == 1) {
            addBook();
        }
        if (choice == 2) {
            readBook();
        }
        if (choice == 3) {
            rearrange();
        }
        if (choice == 4) {
            puts("Bye.");
            exit(0);
        }
    }
}