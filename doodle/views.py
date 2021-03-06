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


    def post(self, request): #uncomment to add artist id to image
        request.data['user_artist'] = request.user.id
        print('User iD====:', request.user.id)
        print('DATAAAAAAAAAAAAAAAAA====:', request.data)
        # correct_answer = CorrectAnswer(correct_answer = request.data['correct_answer'])
        # images = ImageSerializer(data=request.data)
        image = Image(user_drawn_image=request.FILES['user_drawn_image'])
        # image = Image(user_drawn_image=request.FILES['user_drawn_image'], correct_answer=correct_answer)
        print('AFTERr  first  serializer====:', image)
        # if images.is_valid():
        # correct_answer.save()
            # image.save()
        image.save()
        # imageId.save()
        return Response('Success')

    # def put(self, request, pk):
    #     # request.data['correct_answer'] = request.user.id
    #     image = Image.objects.get(pk=pk)
    #     # if image.owner.id != request.user.id:
    #         # return Response(status=HTTP_401_UNAUTHORIZED)
    #     updated_image = ImageSerializer(image, data=request.data)
    #     if (updated_image.is_valid()):
    #         updated_image.save()
    #         return Response(updated_image.data)
    #     return Response(updated_image.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)

    # def post(self, request):  # uncomment to add artist id to image
    #     request.data['user_artist'] = request.user.id
    #     images = ImageSerializer(data=request.data)
    #     image = Image(user_drawn_image=request.FILES['user_drawn_image'])
    #     if images.is_valid():
    #         # image.save()
    #         images.save()
    #     # imageId.save()
    #     return Response('Success')
    #     # print('User iD====:', request.correct_answer)
    #     # images = ImageSerializer(data=request.data)
    #     # print('After serializwer====:', images)
    #     # # imageId = ImageSerializer(data=request.data)
    #     # image = Image(user_drawn_image=request.FILES['user_drawn_image'])
    #     # print('User second serializer====:', image)
    #     # if images.is_valid():
    #     #     # image.save()
    #     #     images.save()
    #     #     # imageId.save()
    #     #     return Response(images.data, status=HTTP_201_CREATED)
    #     # return Response(images.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)



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
        print('userid', request.user.id)
        answer = UserAnswerSerializer(data=request.data)
        print('userid', answer)
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
        request.data['user_artist'] = request.user.id
        user_answer = CorrectAnswerSerializer(data=request.data)
        if user_answer.is_valid():
            user_answer.save()
            return Response(user_answer.data, status=HTTP_201_CREATED)
        return Response(user_answer.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


class DetailImageView(APIView):
    def get(self, request, pk):
        image = Image.objects.get(pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)
    
    def put(self, request, pk):
        request.data['user_artist'] = request.user.id
        # request.data['correct_answer'] = request.user.id
        image = Image.objects.get(pk=pk)
        # if image.owner.id != request.user.id:
            # return Response(status=HTTP_401_UNAUTHORIZED)
        print('PUT REQUEST with pk value:', pk)
        updated_image = ImageSerializer(image, data=request.data)
        if (updated_image.is_valid()):
            updated_image.save()
            return Response(updated_image.data)
        return Response(updated_image.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)



class DetailAnswerView(APIView):
    def get(self, request, pk):
        answer = CorrectAnswer.objects.get(pk=pk)
        serializer = CorrectAnswerSerializer(answer)
        return Response(serializer.data)


# £££££££££££££££££
# class ImageView(APIView):
#     def get(self, request):
#         images = Image.objects.all()
#         serializer = ImageSerializer(images, many=True)
#         return Response(serializer.data)

#     def post1(self, request): #uncomment to add artist id to image
#         print('User iD====:', request.user.id)
#         print('User asdasdasdasdiD====:', request.data)
#         request.data['user_artist'] = request.user.id
#         # print('User iD====:', request.correct_answer)
#         images = ImageSerializer(data=request.data)
#         print('After serializwer====:', images)
#         # imageId = ImageSerializer(data=request.data)
#         image = Image(user_drawn_image=request.FILES['user_drawn_image'])
#         print('User second serializer====:', image)
#         if images.is_valid():
#             image.save()
#             # image.save()
#             images.save()
#             # imageId.save()
#             return Response(images.data, status=HTTP_201_CREATED)
#         return Response(images.errors, status=HTTP_422_UNPROCESSABLE_ENTITY)


#     def post(self, request): #uncomment to add artist id to image
#         request.data['user_artist'] = request.user.id
#         print('User iD====:', request.user.id)
#         print('DATAAAAAAAAAAAAAAAAA====:', request.data)
#         # correct_answer = CorrectAnswer(correct_answer = request.data['correct_answer'])
#         # images = ImageSerializer(data=request.data)
#         image = Image(user_drawn_image=request.FILES['user_drawn_image'])
#         # image = Image(user_drawn_image=request.FILES['user_drawn_image'], correct_answer=correct_answer)
#         print('AFTERr  first  serializer====:', image)
#         # if images.is_valid():
#         # correct_answer.save()
#             # image.save()
#         image.save()
#         # imageId.save()
#         return Response('Success')

class DetailUserView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

