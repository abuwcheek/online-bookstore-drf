from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Cart, CartItem
from .serializers import CartSerializers, CartItemSerializers, CartStatusUpdateSerializers
from apps.books.models import Book



class CartRetrieveView(RetrieveAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CartSerializers

     def get_object(self):
          cart, created = Cart.objects.get_or_create(user=self.request.user)
          return cart



class CartItemCreateView(CreateAPIView):
     permission_classes = [IsAuthenticated]
     serializer_class = CartItemSerializers

     def create(self, request, *args, **kwargs):
          user = request.user 
          cart, created = Cart.objects.get_or_create(user=user)

          book_id = request.data.get('book')
          quantity = int(request.data.get('quantity', 1))

          book = Book.objects.filter(id=book_id).first()

          if not book:
               data = {
                    'status': False,
                    'message': "kitob id si topilmadi"
               }
               return Response(data=data, status=status.HTTP_404_NOT_FOUND)
          
          cart_item, created = CartItem.objects.get_or_create(cart_id=cart.id, book=book)

          if not created:
               if cart_item.quantity + quantity > 10:
                    data = {
                         'status': False, 
                         'message': "bir xil kitobdan 10tadan ortiq qo'sha olmaysiz"
                    }
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
               cart_item.quantity += quantity

          else:
               cart_item.quantity = min(quantity, 10)

          cart_item.save()
          data = {
               'status': True,
               'message': "kitob cart ga qo'shildi",
               'data': CartItemSerializers(cart_item).data
          }
          return Response(data=data, status=status.HTTP_201_CREATED)



class CartItemDestroyView(DestroyAPIView):
     permission_classes = [IsAuthenticated]

     def delete(self, request, *args, **kwargs):
          user = request.user
          book = self.kwargs['book_id']

          cart_item = CartItem.objects.filter(cart__user=user, book=book).first()
          if not cart_item:
               data = {
                    'status': False,
                    'message': "bu kitob cart da mavjud emas"
               }
               return Response(data=data)

          cart_item.delete()
          data = {
               'status': True,
               'message': "kitob cart dan o'chirildi"
          }

          return Response(data=data)



class CartClearView(DestroyAPIView):
     permission_classes = [IsAuthenticated]

     def delete(self, request, *args, **kwargs):
          user = request.user
          cart = Cart.objects.filter(user=user).first()

          if not cart:
               return Response({"status": False, "message": "Sizda mavjud cart yo‘q"}, status=status.HTTP_404_NOT_FOUND)

          # Foydalanuvchining barcha cart itemlarini o‘chirish
          cart.items.all().delete()

          return Response({"status": True, "message": "Savatcha tozalandi"}, status=status.HTTP_204_NO_CONTENT)



class CartStatusUpdateView(UpdateAPIView):
     permission_classes = [IsAdminUser]
     serializer_class = CartStatusUpdateSerializers
     queryset = CartItem.objects.filter(is_active=True)

     def update(self, request, *args, **kwargs):
          order = self.get_object()
          serializer = self.get_serializer(order, data=request.data, partial=True)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          data = {
               'status': True,
               'message': "buyurtma statusi o'zgardi"
          }

          return Response(data=data)          



class CartHistoryAPIView(APIView):
     permission_classes = [IsAuthenticated]

     def get(self, request):
          user = request.user
          orders = Cart.objects.filter(user=user)  

          if not orders.exists():
               data = {
                    'status': False,
                    'message': "Siz hali hech qanday buyurtma bermagansiz",
                    'data': []
               }
               return Response(data=data)

          data = {
               'status': True,
               'message': "Buyurtmalar tarixi",
               'orders': CartSerializers(orders, many=True).data  
          }
          return Response(data=data)
