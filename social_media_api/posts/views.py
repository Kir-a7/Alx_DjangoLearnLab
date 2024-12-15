from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from .models import Post, Comment,Like
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from rest_framework import filters


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        following_users = request.user.following.all()

        posts = Post.objects.filter(author__in=following_users).order_by("-created_at")
        feed_data = [
            {
                "id": post.id,
                "author": post.author.username,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
            }
            for post in posts
        ]
        return Response(feed_data, status=status.HTTP_200_OK)


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # Fetch or return 404
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post,
        )
        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_200_OK
        )


class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # Fetch or return 404
        like = Like.objects.filter(user=request.user, post=post)

        if not like.exists():
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like.delete()
        return Response(
            {"detail": "Post unliked successfully."}, status=status.HTTP_200_OK
        )