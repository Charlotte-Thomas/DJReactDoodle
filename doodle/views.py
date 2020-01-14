# Create your views here.

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from django.conf import settings

from rest_framework.views import APIView  # get the APIView class from DRF
from rest_framework.response import Response  # get the Response class from DRF
from rest_framework.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from .models import Image, User, Category, UserAnswer, CorrectAnswer
from .serializers import ImageSerializer, UserSerializer, CategorySerializer, UserAnswerSerializer, CorrectAnswerSerializer

# Create your views here.


class ImageView(APIView):
    def get(self, request):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        # request.data['user_artist'] = request.user.id
        # imageId = ImageSerializer(data=request.data)
        image = Image(user_drawn_image=request.FILES['user_drawn_image'])
        # if imageId.is_valid():
        image.save()
            # imageId.save()
        return Response('Success')


class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        category = CategorySerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, status=HTTP_201_CREATED)
        return Response(category.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class UserAnswerView(APIView):
    def get(self, request):
        answers = UserAnswer.objects.all()
        serializer = UserAnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request):
        # links current user to the post that was made
        request.data['user'] = request.user.id
        answer = UserAnswerSerializer(data=request.data)
        if answer.is_valid():
            answer.save()
            return Response(answer.data, status=HTTP_201_CREATED)
        return Response(answer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class CorrectAnswerView(APIView):
    def get(self, request):
        answers = CorrectAnswer.objects.all()
        serializer = CorrectAnswerSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request):
        # links current user to the post that was made
        request.data['user'] = request.user.id
        user_answer = CorrectAnswerSerializer(data=request.data)
        if user_answer.is_valid():
            user_answer.save()
            return Response(user_answer.data, status=HTTP_201_CREATED)
        return Response(user_answer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)