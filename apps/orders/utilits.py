from django.db import transaction
from apps.orders.models import Cart
from apps.orders.models import Order, OrderItem

def create_order_from_cart(user):
     """
     Foydalanuvchining savatchasidan buyurtma yaratadi.
     """
     cart = Cart.objects.filter(user=user).first()  # Foydalanuvchining savatchasini olish
     if not cart or not cart.items.exists():  # Agar savatcha bo‘sh bo‘lsa
          return None  

     with transaction.atomic():  # Atomik tranzaksiya (xatolik bo‘lsa, hammasi bekor qilinadi)
          order = Order.objects.create(
               user=user,
               total_price=cart.total_price(),  # Savatchadagi umumiy narxni olish
               status="pending"
          )

          # Savatchadagi mahsulotlarni buyurtmaga o‘tkazish
          for item in cart.items.all():
               OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price  # Hozirgi narx saqlanadi
               )

          # Savatchani tozalash
          cart.items.all().delete()

     return order  # Yaratilgan buyurtmani qaytarish
