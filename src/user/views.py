from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer, ProfileSerializer
from django.contrib import messages
from .models import Profile
#from rest_framework import generics


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


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = RegisterSerializer

@api_view(["GET", "PUT"])
def ProfileView(request, id):
    profile = get_object_or_404(Profile, id=id)

    if request.method == "GET":
        serializer = ProfileSerializer(profil)
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
