from django.shortcuts import render, redirect
from .models import Library
from relationship_app.models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def list_books(request):
    books = Book.objects.all()  # Get all Book objects
    return render(request, 'relationship_app/list_books.html', {'books': books})



# Class-based view to display library details and associated books
class LibraryDetailView(DetailView):
    model = Library  # Model to use for this view
    template_name = 'relationship_app/library_detail.html'  # Template to render
    context_object_name = 'library'  # Name to use for the Library instance in the template

    def get_context_data(self, **kwargs):
        # Get the existing context data from the parent class
        context = super().get_context_data(**kwargs)
        
        # Add all books associated with this library to the context
        context['books'] = self.object.books.all()
        
        return context




# View for user registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the homepage after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

