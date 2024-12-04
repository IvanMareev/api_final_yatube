from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet)
router.register('comments', CommentViewSet)
router.register(r'follow', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
