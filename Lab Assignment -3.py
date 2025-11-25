import json
import logging
from pathlib import Path

# Configure Logging

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Book Class

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self):
        self.status = "available"



# Library Inventory with Save/Load JSON

class LibraryInventory:
    def __init__(self, filename="books.json"):
        self.books = []
        self.filename = Path(filename)
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
            return
        for b in self.books:
            print(b)


    def save_books(self):
        try:
            data = [b.to_dict() for b in self.books]
            self.filename.write_text(json.dumps(data, indent=4))
            logging.info("Books saved successfully.")
        except Exception as e:
            logging.error(f"Error saving books: {e}")

    def load_books(self):
        try:
            if not self.filename.exists():
                logging.warning("Book file not found, creating new one.")
                self.filename.write_text("[]")

            data = json.loads(self.filename.read_text())
            for item in data:
                book = Book(
                    item["title"],
                    item["author"],
                    item["isbn"],
                    item["status"]
                )
                self.books.append(book)

            logging.info("Books loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading books: {e}")
            print("Error reading file. Starting with empty inventory.")
            self.books = []



# Menu Driven CLI

def menu():
    inventory = LibraryInventory()

    while True:
        print("\n========== LIBRARY MENU ==========")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")
        print("==================================")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Enter a number.")
            continue

        # Add Book 
        if choice == 1:
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")

            if inventory.search_by_isbn(isbn):
                print("A book with this ISBN already exists.")
                continue

            book = Book(title, author, isbn)
            inventory.add_book(book)
            inventory.save_books()
            print("✔ Book added successfully.")

        # Issue Book
        elif choice == 2:
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)

            if not book:
                print("Book not found.")
            elif not book.is_available():
                print("Book already issued.")
            else:
                book.issue()
                inventory.save_books()
                print("Book issued successfully.")

        # Return Book
        elif choice == 3:
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)

            if not book:
                print("Book not found.")
            else:
                book.return_book()
                inventory.save_books()
                print("Book returned successfully.")

        # View All Books
        elif choice == 4:
            inventory.display_all()

        # Search Book
        elif choice == 5:
            print("\nSearch by:")
            print("1. Title")
            print("2. ISBN")
            try:
                opt = int(input("Enter option: "))
            except ValueError:
                print("Invalid choice.")
                continue

            if opt == 1:
                title = input("Enter title keyword: ")
                results = inventory.search_by_title(title)
                if results:
                    for b in results:
                        print(b)
                else:
                    print("No matching books found.")

            elif opt == 2:
                isbn = input("Enter ISBN: ")
                book = inventory.search_by_isbn(isbn)
                print(book if book else "Book not found.")

        # Exit
        elif choice == 6:
            print("Saving and exiting...")
            inventory.save_books()
            break

        else:
            print("Invalid option. Try again.")


# Run Program

if __name__ == "__main__":
    menu()
