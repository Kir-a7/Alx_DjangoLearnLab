from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Post, Comment, Tag 
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'bio') 


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'bio') 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(),  
            'content': forms.Textarea(attrs={'cols': 80, 'rows': 20}), 
        }


    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            tag_names = {tag.strip() for tag in self.cleaned_data['tags'].split(',') if tag.strip()}
            tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]
            post.tags.set(tags)  
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']