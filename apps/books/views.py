from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Book, BookImage, BookRating, BookLike
from .serializers import (CategoryCreateSerializer, CategoryListSerializer,
                          BookCreateSerializer, BookListSerializer, 
                          BookUpdateSerializers)



class CategoryCreateView(CreateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CategoryCreateSerializer
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
     serializer_class = CategoryCreateSerializer
     queryset = Category.objects.all()

     def delete(self, request, *args, **kwargs):
          instance = self.get_object()
          self.perform_destroy(instance)
          data = {
               'status': True,
               'message': "Category o'chirildi",
          }
          return Response(data=data, status=status.HTTP_200_OK)



class BookCreateView(APIView):
     permission_classes = [IsAdminUser]
     serializer_class = BookCreateSerializer
     
     def post(self, request):
          serializer = self.serializer_class(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          serializer.save()

          data = {
               'status': True,
               'message': "kitob qo'shdingiz\n",
               'data': serializer.data
          }
          return Response(data=data)



class BookListView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = BookListSerializer
     queryset = Book.objects.filter(is_active=True)
     filter_backends = [SearchFilter, OrderingFilter]
     search_fields = ['title', 'author', 'category__name']
     ordering_fields = ['title', 'author', 'price', 'created_at']


     def get_serializer_context(self):
          """
          Serializer uchun contextga `request`ni qo'shamiz.
          Bu `image` URL'sini to‘liq qilish uchun kerak.
          """
          context = super().get_serializer_context()
          context["request"] = self.request
          return context



class BookUpdateView(UpdateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = BookUpdateSerializers
     queryset = Book.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          instance = self.get_object()  # Yangilangan obyektni olish
          response = super().update(request, *args, **kwargs)  # Asosiy update chaqirish
          data = {
               'status': True, 
               'message': "kitobni o'zgartirdingiz\n",
               'data': response.data
          }
          return Response(data=data)



class BookDestroyView(DestroyAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = BookUpdateSerializers
     queryset = Book.objects.filter(is_active=True)

     def delete(self, request, *args, **kwargs):
          super().delete(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "kitobni o'chirib tashladingiz"
          }
          return Response(data=data)