from django.urls import path
from .import views
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns =[
    path('home/', views.home_view, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name = "login"),
    path("logout/", views.user_logout, name ="logout"),
    path("profile/", views.profile, name="profile"),
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:post_id>/comment/new/', views.add_comment, name='add-comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),
 
]
