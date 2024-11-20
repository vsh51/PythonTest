import tabulate
import matplotlib.pyplot as plt

class Book:
    """Class for book representation"""

    def __init__(self, title, author, year, ganre, amount):
        """Initialize book object"""
        self.title = title
        self.author = author
        self.year = year
        self.ganre = ganre
        self.amount = amount

    def __str__(self):
        """Return string representation of book object"""
        return f"{self.title},{self.author},{self.year},{self.ganre},{self.amount}"

    def change_title(self, new_title):
        """Change title of book"""
        self.title = new_title

    def change_author(self, new_author):
        """Change author of book"""
        self.author = new_author

    def change_year(self, new_year):
        """Change year of book"""
        self.year = new_year

    def change_ganre(self, new_ganre):
        """Change ganre of book"""
        self.ganre = new_ganre

    def change_amount(self, new_amount):
        """Change amount of book"""
        self.amount = new_amount


class LibError(BaseException):
    def __init__(self, message):
        self.message = message


class Library:
    """Class for library representation"""

    _id = 0

    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.books = {}

        self.fd = open(self.filename)
        columns = self.fd.readline()

        if columns != "Назва,Автор,Рік видання,Жанр,Кількість примірників\n":
            raise LibError("Invalid file format")

        for line in self.fd:
            title, author, year, ganre, amount = line.strip().split(",")
            amount = int(amount)
            self.books[Library._id] = Book(title, author, year, ganre, amount)
            Library._id += 1

        return self

    def __exit__(self, _1, _2, _3):
        self.fd.close()

    def add_book(self, book):
        for key, value in self.books.items():
            if value.title == book.title:
                value.amount += book.amount
                return
        self.books[Library._id] = book
        Library._id += 1

    def remove_book(self, title):
        for key, value in self.books.items():
            if value.title == title:
                if value.amount > 1:
                    value.amount -= 1
                    return
                if value.amount == 1:
                    del self.books[key]
                    return
        raise LibError("Book not found")

    def total_amount(self):
        return sum([int(book.amount) for book in self.books.values()])

    def authors_books(self, author):
        books = [value for value in self.books.values() if value.author == author]
        return books if books else None

    def year_books(self, year):
        books = [value for value in self.books.values() if value.year == year]
        return books if books else None

    def most_popular_ganre(self):
        ganres = {}
        for value in self.books.values():
            if value.ganre in ganres:
                ganres[value.ganre] += 1 * value.amount
            else:
                ganres[value.ganre] = 1 * value.amount

        max_ganre_value = max(ganres.values())
        ganres = [key for key, value in ganres.items() if value == max_ganre_value]
        
        return ", ".join(ganres)

    def __str__(self):
        return tabulate.tabulate(
            [(key, value.title, value.author, value.year, value.ganre, value.amount) for key, value in self.books.items()],
            headers=["ID", "Title", "Author", "Year", "Ganre", "Amount"],
            tablefmt="grid"
        )

def main():
    with Library("library.csv") as library:
        print(library)
        
        """Menu"""
        while True:
            try:
                print()
                print("1. Add book")
                print("2. Edit book")
                print("3. Remove book")
                print("5. Show all books")
                print("6. Total amount of books")
                print("7. Most popular ganre")
                print("8. Author's books")
                print("9. Books by year")
                print("10. Pie chart of ganres")
                print("11. Histogram of years")
                print("12. Exit")
                choice = int(input("Enter choice: "))

                if choice == 1:
                    title = input("Enter title: ")
                    author = input("Enter author: ")
                    year = input("Enter year: ")
                    ganre = input("Enter ganre: ")
                    amount = int(input("Enter amount: "))
                    library.add_book(Book(title, author, year, ganre, amount))

                elif choice == 2:
                    id = int(input("Enter ID of book to edit: "))
                    field = input("Enter field to edit: ")
                    field = field.lower()
                    new_value = input("Enter new value: ")
                    if field == "title":
                        library.books[id].change_title(new_value)
                    elif field == "author":
                        library.books[id].change_author(new_value)
                    elif field == "year":
                        library.books[id].change_year(new_value)
                    elif field == "ganre":
                        library.books[id].change_ganre(new_value)
                    elif field == "amount":
                        library.books[id].change_amount(new_value)
                    else:
                        raise LibError("Invalid field")

                elif choice == 3:
                    title = input("Enter title of book to remove: ")
                    library.remove_book(title)

                elif choice == 5:
                    print(library)

                elif choice == 6:
                    print(library.total_amount())

                elif choice == 7:
                    print(library.most_popular_ganre())

                elif choice == 8:
                    author = input("Enter author: ")
                    books = library.authors_books(author)
                    if books:
                        print(tabulate.tabulate(
                            [(book.title, book.author, book.year, book.ganre, book.amount) for book in books],
                            headers=["Title", "Author", "Year", "Ganre", "Amount"],
                            tablefmt="grid"
                        ))
                    else:
                        raise LibError("Author not found")

                elif choice == 9:
                    year = input("Enter year: ")
                    books = library.year_books(year)
                    if books:
                        print(tabulate.tabulate(
                            [(book.title, book.author, book.year, book.ganre, book.amount) for book in books],
                            headers=["Title", "Author", "Year", "Ganre", "Amount"],
                            tablefmt="grid"
                        ))
                    else:
                        raise LibError("Year not found")

                elif choice == 10:
                    ganres = {}
                    for value in library.books.values():
                        if value.ganre in ganres:
                            ganres[value.ganre] += 1 * value.amount
                        else:
                            ganres[value.ganre] = 1 * value.amount
                    plt.pie(ganres.values(), labels=ganres.keys(), autopct="%1.1f%%")
                    plt.show()

                elif choice == 11:
                    years = {}
                    for value in library.books.values():
                        if value.year in years:
                            years[value.year] += 1 * value.amount
                        else:
                            years[value.year] = 1 * value.amount
                    plt.bar(years.keys(), years.values())
                    plt.show()

                elif choice == 12:
                    break

            except Exception as e:
                print(f"Error: {e}")
            except ValueError:
                print("Invalid input")
            except LibError as e:
                print(f"Error: {e}")
if __name__ == "__main__":
    main()
