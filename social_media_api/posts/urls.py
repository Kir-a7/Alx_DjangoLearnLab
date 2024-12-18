from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet,LikePostView, UnlikePostView
from django.urls import path,include
from .views import FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet)
urlpatterns = router.urls

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
    path('', include(router.urls)),
    
]



