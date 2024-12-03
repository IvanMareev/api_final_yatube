from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.relations import PrimaryKeyRelatedField
from posts.models import Comment, Post, Group, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True)
    following = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'user': instance.user.username,
            'following': instance.following.username,
        }
