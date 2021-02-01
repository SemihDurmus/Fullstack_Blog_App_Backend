from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, ProfileSerializer, UserSerializer
from django.contrib import messages
from .models import Profile

# -------------------REGISTER----------------------


@api_view(["POST"])
def RegisterView(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if request.user.is_authenticated:
            messages.warning(request, "You already have an account!")
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "{} created successfully!".format(serializer.validated_data['username'])
            }
            return Response(data, status=status.HTTP_201_CREATED)
        data = {
            "message": "User could not be created !"
        }
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -------------------USER GET UPDATE DELETE----------------------


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def UserGetUpdateDelete(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "Password updated successfully"
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------PROFILE VIEW----------------------


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def ProfileView(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == "GET":
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "profile updated successfully"
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
