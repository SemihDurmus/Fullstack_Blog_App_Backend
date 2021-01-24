from rest_framework import serializers
from .models import Category, Post, Comment, Like, PostView
from django.db.models.query_utils import Q


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "post_count"
        )


class CommentSerializer(serializers.ModelSerializer):

    commenter = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = (
            "commenter",
            "post",
            "time_stamp",
            "content"
        )


class PostSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Post.OPTIONS)
    comments = CommentSerializer(many=True, required=False)
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image_URL",
            "category",
            "publish_date",
            "update_date",
            "author",
            "author_avatar",
            "status",
            "is_liked",
            "slug",
            "comment_count",
            "like_count",
            "view_count",
            "comments"
        )

    def get_is_liked(self, obj):
        request = self.context['request']
        if request.user.is_authenticated:
            if Post.objects.filter(Q(like__user=request.user) & Q(like__post=obj)).exists():
                return True
            return False


class PostEditSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image_URL",
            "category",
            "update_date",
            "author_avatar",
            "status",
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "user",
            "post",
        )


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = (
            "user",
            "post",
            "time_stamp"
        )
