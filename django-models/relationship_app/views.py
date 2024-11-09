from django.shortcuts import render
from relationship_app.models import Book, Library
from django.views.generic import DetailView

def list_books(request):
    books = Book.objects.all()  # Get all Book objects
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library  # Specify the model this view will work with
    template_name = 'relationship_app/library_detail.html'  # Template to render
    context_object_name = 'library' 