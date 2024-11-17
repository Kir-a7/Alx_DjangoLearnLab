from .models import Author, Library


objects.filter(author=author)
Author.objects.get(name=author_name)

books = Library.objects.all()
Librarian.objects.get(library=)
Library.objects.get(name=library_name)
books.all()

