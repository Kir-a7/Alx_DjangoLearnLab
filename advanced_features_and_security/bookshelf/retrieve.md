book = Book.objects.get()
book.title, book.author, book.publication_year
# Expected output: ('1984', 'George Orwell', 1949)