from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment

def home_view(request):
   
    return render(request, 'blog/base.html')

def register(request):
    if request.method =="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
        
        else:
            form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})    
        

def user_login (request):
    if request.method == "POST":
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
        else:
            form= AuthenticationForm()
        return render(request, "login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect ("login") 

@login_required 
def profile(request):
    return render (request, "profile.html", {"user": request.user})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, isinstance= request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        else:
            form = UserChangeForm(isinstance = request.user)
        return render (request, "profile.html", {"form": form})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' 

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')  # Redirect to the list after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post_id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post-detail', pk=comment.post.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('post-detail', pk=comment.post.id)