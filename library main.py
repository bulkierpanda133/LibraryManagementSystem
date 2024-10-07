import datetime

class Book:
    def __init__(self, title, author, genre, available=True):
        self.title = title
        self.author = author
        self.genre = genre
        self.available = available
        self.due_date = None
        self.borrower = None
        self.reservations = []

    def is_available(self):
        return self.available

    def borrow(self, user):
        if self.is_available():
            self.available = False
            self.borrower = user
            self.due_date = datetime.datetime.now() + datetime.timedelta(days=14)  # 2 weeks
            print(f"Book '{self.title}' borrowed by {user.name}. Due date: {self.due_date.strftime('%Y-%m-%d')}")
        else:
            print(f"Book '{self.title}' is currently unavailable.")

    def return_book(self):
        if not self.is_available():
            if self.due_date < datetime.datetime.now():
                overdue_days = (datetime.datetime.now() - self.due_date).days
                fine = overdue_days * 1  # $1 per day
                print(f"Book '{self.title}' is overdue by {overdue_days} days. Fine: ${fine}")
                return fine
            else:
                print(f"Book '{self.title}' returned on time.")
            self.available = True
            self.borrower = None
            self.due_date = None
            self.process_reservation()
        else:
            print(f"Book '{self.title}' is not borrowed.")

    def add_reservation(self, user):
        self.reservations.append(user)
        print(f"User '{user.name}' has reserved '{self.title}'.")

    def process_reservation(self):
        if self.reservations:
            user = self.reservations.pop(0)  # Notify the first user in the queue
            print(f"Notification: Book '{self.title}' is now available for {user.name}.")
            user.reserve_book(self)

class User:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.borrowed_books = []
        self.fine = 0

    def borrow_book(self, book):
        book.borrow(self)
        if book.is_available():
            self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            fine = book.return_book()
            if fine:
                self.fine += fine
            self.borrowed_books.remove(book)
        else:
            print(f"You haven't borrowed '{book.title}'.")

    def reserve_book(self, book):
        book.add_reservation(self)

    def pay_fine(self, amount):
        if amount >= self.fine:
            print(f"Fine of ${self.fine} paid.")
            self.fine = 0
        else:
            self.fine -= amount
            print(f"${amount} paid. Remaining fine: ${self.fine}")

class Author:
    def __init__(self, name, biography):
        self.name = name
        self.biography = biography

class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.authors = []
        self.load_data()

    def load_data(self):
        self.load_books()
        self.load_users()
        self.load_authors()

    def save_data(self):
        self.save_books()
        self.save_users()
        self.save_authors()

    def load_books(self):
        try:
            with open("books.txt", "r") as f:
                for line in f:
                    title, author, genre, available = line.strip().split(",")
                    book = Book(title, author, genre, available == "Available")
                    self.books.append(book)
        except FileNotFoundError:
            print("Books file not found. Starting with an empty book list.")
        except Exception as e:
            print(f"Error loading books: {e}")

    def save_books(self):
        try:
            with open("books.txt", "w") as f:
                for book in self.books:
                    f.write(f"{book.title},{book.author},{book.genre},{ 'Available' if book.is_available() else 'Unavailable' }\n")
        except Exception as e:
            print(f"Error saving books: {e}")

    def load_users(self):
        try:
            with open("users.txt", "r") as f:
                for line in f:
                    name, user_id = line.strip().split(",")
                    user = User(name, user_id)
                    self.users.append(user)
        except FileNotFoundError:
            print("Users file not found. Starting with an empty user list.")
        except Exception as e:
            print(f"Error loading users: {e}")

    def save_users(self):
        try:
            with open("users.txt", "w") as f:
                for user in self.users:
                    f.write(f"{user.name},{user.user_id}\n")
        except Exception as e:
            print(f"Error saving users: {e}")

    def load_authors(self):
        try:
            with open("authors.txt", "r") as f:
                for line in f:
                    name, biography = line.strip().split(",")
                    author = Author(name, biography)
                    self.authors.append(author)
        except FileNotFoundError:
            print("Authors file not found. Starting with an empty author list.")
        except Exception as e:
            print(f"Error loading authors: {e}")

    def save_authors(self):
        try:
            with open("authors.txt", "w") as f:
                for author in self.authors:
                    f.write(f"{author.name},{author.biography}\n")
        except Exception as e:
            print(f"Error saving authors: {e}")

    def add_book(self, title, author, genre):
        book = Book(title, author, genre)
        self.books.append(book)
        self.save_books()  # Save after adding

    def add_user(self, name, user_id):
        user = User(name, user_id)
        self.users.append(user)
        self.save_users()  # Save after adding

    def add_author(self, name, biography):
        author = Author(name, biography)
        self.authors.append(author)
        self.save_authors()  # Save after adding

    def find_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def find_book_by_title(self, title):
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def display_books(self):
        for book in self.books:
            status = "Available" if book.is_available() else "Unavailable"
            print(f"{book.title} by {book.author} - {status}")

    def display_users(self):
        for user in self.users:
            print(f"{user.name} (ID: {user.user_id}) - Fine: ${user.fine}")

    def display_authors(self):
        for author in self.authors:
            print(f"{author.name}: {author.biography}")

class LibraryManagementSystem:
    def __init__(self):
        self.library = Library()

    def run(self):
        while True:
            print("\nWelcome to the Library Management System!")
            print("1. Book Operations")
            print("2. User Operations")
            print("3. Author Operations")
            print("4. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.book_operations()
            elif choice == "2":
                self.user_operations()
            elif choice == "3":
                self.author_operations()
            elif choice == "4":
                self.library.save_data()  # Save all data on exit
                print("Exiting the Library Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def book_operations(self):
        while True:
            print("\nBook Operations:")
            print("1. Add Book")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Search Book")
            print("5. Display All Books")
            print("6. Back to Main Menu")
            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                genre = input("Enter book genre: ")
                self.library.add_book(title, author, genre)
            elif choice == "2":
                user_id = input("Enter your user ID: ")
                user = self.library.find_user_by_id(user_id)
                if user:
                    book_title = input("Enter the title of the book you want to borrow: ")
                    book = self.library.find_book_by_title(book_title)
                    if book:
                        user.borrow_book(book)
                    else:
                        print("Book not found.")
                else:
                    print("User not found.")
            elif choice == "3":
                user_id = input("Enter your user ID: ")
                user = self.library.find_user_by_id(user_id)
                if user:
                    book_title = input("Enter the title of the book you want to return: ")
                    book = self.library.find_book_by_title(book_title)
                    if book:
                        user.return_book(book)
                    else:
                        print("Book not found.")
                else:
                    print("User not found.")
            elif choice == "4":
                title = input("Enter the title of the book to search: ")
                book = self.library.find_book_by_title(title)
                if book:
                    print(f"Found: {book.title} by {book.author} - {'Available' if book.is_available() else 'Unavailable'}")
                else:
                    print("Book not found.")
            elif choice == "5":
                self.library.display_books()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def user_operations(self):
        while True:
            print("\nUser Operations:")
            print("1. Add User")
            print("2. View User Details")
            print("3. Display All Users")
            print("4. Pay Fine")
            print("5. Back to Main Menu")
            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                name = input("Enter user name: ")
                user_id = input("Enter user ID: ")
                self.library.add_user(name, user_id)
            elif choice == "2":
                user_id = input("Enter user ID: ")
                user = self.library.find_user_by_id(user_id)
                if user:
                    print(f"User: {user.name} (ID: {user.user_id}) - Fine: ${user.fine}")
                else:
                    print("User not found.")
            elif choice == "3":
                self.library.display_users()
            elif choice == "4":
                user_id = input("Enter user ID: ")
                user = self.library.find_user_by_id(user_id)
                if user:
                    amount = float(input("Enter amount to pay: "))
                    user.pay_fine(amount)
                else:
                    print("User not found.")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def author_operations(self):
        while True:
            print("\nAuthor Operations:")
            print("1. Add Author")
            print("2. View Author Details")
            print("3. Display All Authors")
            print("4. Back to Main Menu")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                name = input("Enter author name: ")
                biography = input("Enter author biography: ")
                self.library.add_author(name, biography)
            elif choice == "2":
                name = input("Enter author name: ")
                author = next((a for a in self.library.authors if a.name.lower() == name.lower()), None)
                if author:
                    print(f"Author: {author.name} - Biography: {author.biography}")
                else:
                    print("Author not found.")
            elif choice == "3":
                self.library.display_authors()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.run()
