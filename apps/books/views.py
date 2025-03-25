from itertools import count
from django.db.models import Avg, Count
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Book, BookImage, BookRating, Wishlist, View
from .serializers import (CategoryCreateSerializer, CategoryListSerializer,
                          BookCreateSerializer, BookListSerializer, 
                          BookUpdateSerializers, BookRetrieveSerializers, 
                          UserAddWishlistSerializer, UserWishlistSerializer,
                          BookReviewAddSerializer, BookReviewUpdateSerializer,
                          BookReviewListSerializer, BookTopRatingSerializers)



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
          internal_number = request.data.get('internal_number')

          if Book.objects.filter(internal_number=internal_number).exists():
               data = {
                    'status': False,
                    'message': "Bu ichki raqam orqali oldin kitob qo'shilgan",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
          
          serializer = self.serializer_class(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          serializer.save()

          data = {
               'status': True,
               'message': "kitob qo'shdingiz",
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
               'message': "kitobni o'zgartirdingiz",
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



class BookRetrieveView(RetrieveAPIView):
     permission_classes = [AllowAny]
     serializer_class = BookRetrieveSerializers
     queryset = Book.objects.filter(is_active=True)
     
     def retrieve(self, request, *args, **kwargs):
          if request.user.is_authenticated:
               book = self.get_object()
               user = request.user
               view = View.objects.get_or_create(book=book, user=user)
               # view.save()

          return super().retrieve(request, *args, **kwargs)



class UserCreateWishlistView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = UserAddWishlistSerializer

     def get_queryset(self):
          return Wishlist.objects.filter(user=self.request.user)
     
     def create(self, request, *args, **kwargs):
          book_id = request.data.get('book')
          book = get_object_or_404(Book, id=book_id)
          wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, book=book)
          data = {
               'status': True,
               'message': "kitob wishlistga qo'shildi",
               'data': UserAddWishlistSerializer(wishlist_item).data
          }

          if not created:
               data = {
                    'status': False,
                    'message': "Bu kitob allaqachon wishlistda mavjud",
               }
               return Response(data=data)

          return Response(data=data, status=status.HTTP_201_CREATED)



class UserWishlistListView(ListAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = UserWishlistSerializer

     def get_queryset(self):
          return Wishlist.objects.filter(user=self.request.user)



class UserDestoryWishlistView(DestroyAPIView):
     permission_classes = [IsAuthenticated]

     def delete(self, request, *args, **kwargs):
          user = request.user
          book_id = kwargs.get('pk')
          book = get_object_or_404(Book, id=book_id)
          wishlist_item = Wishlist.objects.filter(user=user, book=book).first()
          if not wishlist_item:
               data = {
                    'status': False,
                    'message': "Bu kitob wishlistda mavjud emas",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
          

          wishlist_item.delete()
          data = {
               'status': True,
               'message': "kitob wishlistdan o'chirildi",
          }
          return Response(data=data, status=status.HTTP_200_OK)



class BookReviewAddView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = BookReviewAddSerializer
     queryset = BookRating.objects.all()     


     def create(self, request, *args, **kwargs):
          user = request.user
          book_id = request.data.get('book')
          book = get_object_or_404(Book, id=book_id)
          if BookRating.objects.filter(book=book, user=user).exists() and not user.is_staff:
               data = {
                    'status': False,
                    'message': "Bu kitobga siz oldinroq sharh qoldirdingiz",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          data = {
               'status': True,
               'message': "sharh qoldirdingiz",
               'data': serializer.data
          }
          return Response(data=data, status=status.HTTP_201_CREATED)



class BookReviewUpdateView(UpdateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = BookReviewUpdateSerializer
     queryset = BookRating.objects.all()

     def update(self, request, *args, **kwargs):
          instance = self.get_object()

          if request.user != instance.user:
               data = {
                    'status': False,
                    'message': "Siz faqat o'zingizning sharhingizni o'zgartira olasiz",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

          response = super().update(request, *args, **kwargs)
          data = {
               'status': True,
               'message': "sharhni o'zgartirdingiz",
               'data': response.data
          }
          return Response(data=data)



class BookReviewDestroyView(DestroyAPIView):
     permission_classes = [IsAuthenticated, IsAdminUser]
     serializer_class = BookReviewAddSerializer
     queryset = BookRating.objects.all()

     def delete(self, request, *args, **kwargs):
          instance = self.get_object()

          if request.user != instance.user and not request.user.is_staff:
               data = {
                    'status': False,
                    'message': "Siz faqat o'zingizning sharhingizni o'chira olasiz",
               }
               return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


          self.perform_destroy(instance)
          data = {
               'status': True,
               'message': "sharh o'chirildi",
          }
          return Response(data=data, status=status.HTTP_200_OK)



class BookReviewListView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = BookReviewListSerializer
     queryset = BookRating.objects.all()



class BookTopRatingListView(ListAPIView):
     permission_classes = [AllowAny]
     serializer_class = BookTopRatingSerializers
     
     def get_queryset(self):
          return Book.objects.annotate(
               avg_rating=Avg('ratings__rating'),  # O'rtacha reytingni hisoblash
               review_count=Count('ratings')  # Sharhlar sonini hisoblash
          ).filter(avg_rating__isnull=False).order_by('-avg_rating', '-review_count')[:10]  # Eng yuqori baholangan 10 ta kitob