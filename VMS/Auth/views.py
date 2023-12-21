from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser


class UserRegisterView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user=User.objects.get(username=request.data.get('username'))
            user.set_password(request.data.get('password'))
            user.save()
            token=Token.objects.create(user=user)
            return Response({'token':token.key,'user':serializer.data})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,*args, **kwargs):
        user=get_object_or_404(User,username=request.data.get('username'))
        if not user.check_password(request.data.get('password')):
            return Response("Missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data})
    
    
class UserLogoutView(APIView):
    def get(self,request,*args, **kwargs):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        print(request.user.auth_token)
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)