from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Category, Post, Comment, Like, PostView

from .serializers import CategorySerializer, PostSerializer, CommentSerializer, PostViewSerializer, PostEditSerializer

from django.contrib.auth.decorators import login_required
from rest_framework.pagination import PageNumberPagination

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
        paginator = PageNumberPagination()
        paginator.page_size = 12
        post = Post.objects.all()
        result_page = paginator.paginate_queryset(post, request)
        serializer = PostSerializer(
            result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

# ------------------------POST-CREATE-----------------------


@login_required
@permission_classes([IsAuthenticated])
@api_view(["POST"])
def post_create(request):
    if request.method == "POST":
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            category_serialize = Category(request.data['category'])
            serializer.save(author=request.user, category=category_serialize)
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
@api_view(["GET"])
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "GET":
        if request.user.is_authenticated:
            view = PostView.objects.get_or_create(user=request.user, post=post)
            view_serializer = PostViewSerializer(view, data=request.data)
            if view_serializer.is_valid():
                view_serializer.save()
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)


# ------------------------POST-GET-UPDATE-DELETE---------------------
@login_required
@permission_classes([IsAuthenticated])
@api_view(["GET", "PUT", "DELETE"])
def post_get_update_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "GET":
        get_serializer = PostSerializer(post, context={'request': request})
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

# ------------------------COMMENT CREATE---------------------


@login_required
@api_view(["POST"])
def comment_create_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(commenter=request.user, post=post)
            data = {
                "message": "Comment created successfully!"
            }
        return Response(data, status=status.HTTP_201_CREATED)
    data = {
        "message": "Comment could not be created !"
    }
    return Response(status=status.HTTP_400_BAD_REQUEST)

# ------------------------COMMENT EDIT---------------------


@login_required
@permission_classes([IsAuthenticated])
@api_view(["PUT", "DELETE"])
def comment_edit_view(request, slug, id):
    comment = get_object_or_404(Comment, id=id)
    if request.method == "PUT":
        edit_serializer = CommentSerializer(comment, data=request.data)
        if request.user == comment.commenter:
            if edit_serializer.is_valid():
                edit_serializer.save()
                success_data = {
                    "message": "Comment successfully updated"
                }
                return Response(success_data, status=status.HTTP_202_ACCEPTED)
            return Response(edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        error_data = {
            "message": "You are not the author"
        }
        return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)
    if request.method == "DELETE":
        if request.user == comment.commenter:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        error_data = {
            "message": "Only the author can delete the comment"
        }
        return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)

# -------------------------LIKE VİEW----------------------------------


@login_required()
@api_view(["POST"])
def like(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=post)
        if like_qs.exists():
            like_qs[0].delete()
            data = {
                "message": "Like deleted!"
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        else:
            Like.objects.create(user=request.user, post=post)
            data = {
                "message": "Liked!"
            }
            return Response(data, status=status.HTTP_201_CREATED)
