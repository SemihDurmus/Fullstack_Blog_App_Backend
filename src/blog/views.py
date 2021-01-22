from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Category, Post, Comment, Like, PostView
from .forms import CommentForm

from .serializers import CategorySerializer, PostSerializer, CommentSerializer, LikeSerializer, PostViewSerializer, PostEditSerializer

from django.contrib.auth.decorators import login_required

# ------------------------CATEGORY LIST---------------------


@api_view(["GET"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# ------------------------POST LIST-------------------------


@api_view(["GET"])
def post_list(request):
    if request.method == "GET":
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

# ------------------------POST-CREATE-----------------------


@login_required
@api_view(["POST"])
def post_create(request):
    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Post created successfully!"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": "Post could not be created !"
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------------POST-DETAIL---------------------
@login_required
@api_view(["GET", "POST"])
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "GET":
        if request.user.is_authenticated:
            PostView.objects.get_or_create(user=request.user, post=post)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

        data = {
            "message": "Serializer works"
        }
        return Response(data, status=status.HTTP_202_ACCEPTED)

        # like = get_object_or_404(Like, slug=slug)
        # serializer = LikeSerializer(post)
        # like_qs = Like.objects.filter(user=request.user, post=post)

        # if like_qs:
        #     like_qs[0].delete()

        # else:
        #     Like.objects.create(user=request.user, post=obj)

        return Response(status=status.HTTP_403_FORBIDDEN)


# ------------------------POST-GET-UPDATE-DELETE---------------------
@login_required
@api_view(["GET", "PUT", "DELETE"])
def post_get_update_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "GET":
        get_serializer = PostSerializer(post)
        return Response(get_serializer.data)

    if request.method == "PUT":
        edit_serializer = PostEditSerializer(post, data=request.data)
        if request.user == post.author:
            if edit_serializer.is_valid():
                edit_serializer.save()
                success_data = {
                    "message": "Post successfully updated"
                }
                return Response(success_data, status=status.HTTP_202_ACCEPTED)
            return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error_data = {
            "message": "You are not the author"
        }
        return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "DELETE":
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error_data = {
            "message": "Only the author can delete the post"
        }
        return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)
