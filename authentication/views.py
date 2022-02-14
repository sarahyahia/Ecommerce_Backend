from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework import status, authentication, permissions






class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                # user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
                # user =User.objects.get(request.data.get('username'))
                # print(user,request.POST['username'], request.POST['password'])
                # token = Token.objects.create(user=user) #'user': serializer.data , 'token': token,
            except Exception as e:
                return Response(data={
                        "success":False,
                        "errors":str(e)
                },status=status.HTTP_400_BAD_REQUEST)
            return Response({ "message":"User has been created successfully"}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        try:
            user = User.objects.get(username=username)
            if not(hasattr(user, 'auth_token')) :
                Token.objects.create(user= user)
        except Exception as e:
            return Response({'error': 'User not found', 'errors': str(e)}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response({'error': 'Account is deactivated.'}, status=status.HTTP_401_UNAUTHORIZED)

        user = auth.authenticate(username=username, password=password)
        if user:
            serializer = UserSerializer(user)
            data = {
                'user': serializer.data, 
                "token":user.auth_token.key, 
                'msg':'you have logged in successfully'
            }

            return Response(data, status=status.HTTP_200_OK)
            # SEND RES
        return Response({'error': 'Wrong password'}, status=status.HTTP_401_UNAUTHORIZED)





class LogoutView(GenericAPIView):
    def get(self, request, format=None):
        #delete the token to force a login
        request.user.auth_token.delete() 
        
        return Response(data={
            'success': True,
            'msg': 'logged out successfully'
        }, status=status.HTTP_200_OK)


class DeactivateView(GenericAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user=request.user
        
        if user:
            user.is_active = not(user.is_active)
            user.save()
            return Response(data={'msg':'Deactivated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
        