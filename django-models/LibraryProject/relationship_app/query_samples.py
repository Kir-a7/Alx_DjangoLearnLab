author = Author.objects.get(name="Author Name")
books_by_author = author.books.all()
for book in books_by_author:
    print(book.title)

library = Library.objects.get(name="Library Name")
books_in_library = library.books.all()
for book in books_in_library:
    print(book.title)

library = Library.objects.get(name="Library Name")
librarian = library.librarian
print(librarian.name)
