from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404    
from rest_framework.response import Response
from .models import CustomUser
from .serializers import (CustomUserRegisterSerializers, LogInUserSerializers, 
                          CustomUserViewProfileSerializers, CustomUserUpdateSerializers)



class CustomUserRegisterView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          serializer = CustomUserRegisterSerializers(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = {
               'status': True,
               'message': "muvaffaqiyatli ro'yxatdan o'tdingiz",
               'data': serializer.data
          }
          return Response(data=data)
     


class LogInUserView(APIView):
     permission_classes = [AllowAny]

     def post(self, request):
          serializer = LogInUserSerializers(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.validated_data['user']

          
          # Foydalanuvchi uchun JWT token yaratish
          refresh = RefreshToken.for_user(user)

          data = {
               'status': True,
               'message': "tizimga muvaffaqiyatli kirdingiz",
               'data': {
                    'username': user.username,
                    'email': user.email,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
               }
          }
          return Response(data=data)



class LogoutUserView(APIView):
     permission_classes = [IsAuthenticated]

     def post(self, request):
          tokens = OutstandingToken.objects.filter(user=request.user)
          for token in tokens:
               BlacklistedToken.objects.get_or_create(token=token)
               data = {
                    'status': True,
                    'message': "tizimdan muvaffaqiyatli chiqdingiz"
               }
          return Response(data=data)



class CustomUserViewProfileView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
          user = get_object_or_404(CustomUser, id=request.user.id)
          serializer = CustomUserViewProfileSerializers(user, context={'request': request})

          data = {
               'status': True,
               'data': serializer.data
          }
          return Response(data=data)



class CustomUserUpdateView(APIView):
     permission_classes = [IsAuthenticated]

     def put(self, request):
          user = get_object_or_404(CustomUser, id=request.user.id)
          serializer = CustomUserUpdateSerializers(user, data=request.data, partial=True)

          serializer.is_valid(raise_exception=True)
          serializer.save()
          
          data = {
               'status': True,
               'message': "profile ma'lumotlari muvaffaqiyatli yangilandi",
               'data': serializer.data
          }
          return Response(data=data)



class CustomUserDestroyView(DestroyAPIView):
     permission_classes = [IsAuthenticated]
     
     def delete(self, request):
          user = get_object_or_404(CustomUser, id=request.user.id)
          user.delete()

          data = {
               'status': True,
               'message': "sizning profiliz muvaffaqiyatli o'chirildi"
          }
          return Response(data=data)