book.title = "Nineteen Eighty-Four"
book.save()
updated_book = Book.objects.get(id=book.id)
updated_book.title
# Expected output: 'Nineteen Eighty-Four'
