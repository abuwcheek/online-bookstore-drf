from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Book, BookImage, BookRating, BookLike
from .serializers import CategorySerializer, CategoryListSerializer



class CategoryCreateView(CreateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategorySerializer
     queryset = Category.objects.all()

     def post(self, request):
          category_name = request.data.get('name')
          if Category.objects.filter(name=category_name).exists():
               data = {
                    'status': False,
                    'message': "Bu category oldin mavjud",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
          
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = {
               'status': True,
               'message': "Category qo'shildi",
               'data': serializer.data,
          }     
          return Response(data=data, status=status.HTTP_201_CREATED)



class CategoryListView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = CategoryListSerializer
     queryset = Category.objects.filter(is_active=True)
     filter_backends = [SearchFilter, OrderingFilter]
     search_fields = ['name']



class CategoryDestroyView(DestroyAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategorySerializer
     queryset = Category.objects.all()

     def delete(self, request, *args, **kwargs):
          instance = self.get_object()
          self.perform_destroy(instance)
          data = {
               'status': True,
               'message': "Category o'chirildi",
          }
          return Response(data=data, status=status.HTTP_200_OK)