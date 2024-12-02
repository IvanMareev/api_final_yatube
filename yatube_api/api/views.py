from django.contrib.auth.models import User
from rest_framework import viewsets
from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @action(detail=True, methods=['post'])
    # def comment(self, request, pk=None):
    #     post = self.get_object()
    #     serializer = CommentSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save(author=self.request.user, post=post)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=Post.objects.get(pk=self.kwargs['post_pk']))