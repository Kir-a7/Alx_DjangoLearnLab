from django.shortcuts import render, redirect
from .models import Library
from relationship_app.models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

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


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

