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



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"message": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like = Like.objects.create(post=post, user=request.user)

        # Create a notification for the post author
        notification = Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked",
            target=post,
            target_content_type=ContentType.objects.get_for_model(Post),
        )
        return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like = Like.objects.filter(post=post, user=request.user).first()
        if not like:
            return Response({"message": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        like.delete()
        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)