from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.urls import path
from .views import FeedView

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
]


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)


urlpatterns = router.urls
