from django.shortcuts import render
from relationship_app.models import Book


def list_books(request):
    books = Book.objects.all()  # Get all Book objects
    return render(request, 'relationship_app/list_books.html', {'books': books})
