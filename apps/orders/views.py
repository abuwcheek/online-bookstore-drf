from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from apps.orders.utilits import create_order_from_cart
from apps.users.models import CustomUser
from .models import Cart, CartItem, Order
from .serializers import CartSerializers, CartItemSerializers, CartStatusUpdateSerializers, OrderSerializer
from apps.books.models import Book
from .permissions import IsSuperAdmin



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



class AdminStatsView(APIView):
     permission_classes = [IsSuperAdmin]  # Faqat adminlar uchun ruxsat

     def get(self, request):
          data = {
               "total_users": CustomUser.objects.count(),
               "active_users": CustomUser.objects.filter(is_active=True).count(),
               "total_books": Book.objects.count(),
               "total_orders": Cart.objects.count(),
          }
          return Response(data)



class CreateOrderView(APIView):
     """
     Savatchadagi mahsulotlarni buyurtmaga o'tkazish   
     """
     permission_classes = [IsAuthenticated]  # Faqat login bo'lganlar foydalanishi mumkin

     def post(self, request):
          user = request.user
          order = create_order_from_cart(user)  # Savatchadagi mahsulotlarni buyurtmaga o‘tkazamiz

          if not order:
               data = {
                    'status': False,
                    "message": "savatchangiz bo‘sh!"
               }
               return Response(data=data)

          data = {
               'status': True,
               'message': 'orderga qo\'shildi',
               'data': OrderSerializer(order).data,
          }
          return Response(data=data)  # Buyurtmani JSON formatda qaytaramiz



class UserOrdersView(ListAPIView):
     """
     Foydalanuvchi o'z buyurtmalarini ko'rishi mumkin
     Admin esa barcha buyurtmalarni ko'rishi mumkin
     """
     serializer_class = OrderSerializer
     permission_classes = [IsAuthenticated]

     def get_queryset(self):
          user = self.request.user
          if user.is_staff:
               return Order.objects.all()  # Admin barcha buyurtmalarni ko'radi
          return Order.objects.filter(user=user)  # Oddiy user faqat o'z buyurtmalarini ko'radi



class UpdateOrderStatusView(APIView):
     permission_classes = [IsAdminUser]  # Faqat adminlar uchun

     def patch(self, request, order_id):
          order = get_object_or_404(Order, id=order_id)
          new_status = request.data.get("status")

          if new_status not in ["pending", "confirmed", "shipped", "delivered", "cancelled"]:
               data = {
                    'status': False,
                    "message": "noto'g'ri status"
               }
               return Response(data=data)
          
          order.status = new_status
          order.save()

          data = {
               'status': True,
               'message': "status o'zgartirildi",
               'data': OrderSerializer(order).data,
          }

          return Response(data=data)



class OrderDeleteView(DestroyAPIView):
     """
     Foydalanuvchi faqat o'zining buyurtmalarini o'chira oladi.
     Admin esa istalgan buyurtmani o'chira oladi.
     """
     permission_classes = [IsAuthenticated]

     def delete(self, request, order_id):
          order = get_object_or_404(Order, id=order_id)

          if request.user != order.user and not request.user.is_staff:
               data = {
                    'status': False,
                    'message': "siz bu buyurtmani o‘chira olmaysiz!"
               }
               return Response(data=data)

          order.delete()
          
          data = {
               'status': True,
               'message': "buyurtma muvaffaqiyatli o‘chirildi!"
          }
          return Response(data=data)



class AddressOrderView(APIView):
     """
     Foydalanuvchi cartdagi mahsulotlardan buyurtma yaratishi mumkin
     """
     def post(self, request):
          user = request.user
          cart = Cart.objects.filter(user=user).first()

          if not cart or not cart.items.exists():
               data = {
                    'status': False,
                    'message': 'cartingiz bo\'sh'
               }
               return Response(data=data)


          address = request.data.get("address")
          phone = request.data.get("phone")


          if not address or not phone:
               data = {
                    'status': False,
                    'message': 'manzil va telefon raqami kerak!'
               }
               return Response(data=data)

          total_price = cart.total_price()

          order = Order.objects.create(
               user=user,
               total_price=total_price,
               address=address,
               phone=phone
          )

          for item in cart.items.all():
               order.items.create(book=item.book, quantity=item.quantity, price=item.total_price())

          cart.items.all().delete()

          data = {
               'status': True,
               'message': 'buyurtmangiz to\'lovga tayyor',
               'data': OrderSerializer(order).data,
          }
          return Response(data=data)



class UpdatePaymentStatusView(APIView):
     """
     Admin buyurtmaning to‘lov statusini o‘zgartira oladi
     """
     permission_classes = [IsAdminUser]

     def patch(self, request, order_id):
          order = get_object_or_404(Order, id=order_id)
          new_status = request.data.get("payment_status")

          if new_status not in ["paid", "failed"]:
               data = {
                    'status': False,
                    'message': "noto‘g‘ri status!"
               }
               return Response(data=data)


          order.payment_status = new_status
          order.save()

          data = {
               'status': True,
               'message': "to‘lov statusi {new_status} ga o‘zgartirildi!"
          }
          return Response(data=data)