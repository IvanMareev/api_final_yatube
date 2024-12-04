from django.contrib.auth.models import User
from rest_framework import viewsets
from posts.models import Post, Group, Comment, Follow
from .serializers import CommentSerializer, FollowSerializer
from .serializers import PostSerializer, GroupSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance = self.get_object()
        if instance.author != self.request.user:
            str = "You do not have permission to delete this post."
            raise PermissionDenied(str)
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'PUT', 'PATCH', 'DELETE'],
            url_path='comments/(?P<comment_id>[^/.]+)')
    def comment_detail(self, request, pk=None, comment_id=None):
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(Comment, pk=comment_id, post=post)

        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            if comment.author != request.user:
                str = 'Редактирование чужого комментария запрещено!'
                raise PermissionDenied(str)
            serializer = CommentSerializer(comment, data=request.data,
                                           partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if comment.author != request.user:
                str = 'Удаление чужого комментария запрещено!'
                raise PermissionDenied(str)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('following__username',)

    def list(self, request):
        queryset = Follow.objects.filter(user=request.user)
        sq = request.query_params.get('search', None)
        if sq:
            sq = sq
            queryset = queryset.filter(following__username__icontains=sq)
        serializer = FollowSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        following_user = self.request.data.get('following')
        user = get_object_or_404(User, username=following_user)
        if serializer.is_valid():
            serializer.save(user=self.request.user, following=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
