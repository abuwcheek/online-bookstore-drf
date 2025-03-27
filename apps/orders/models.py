from django.db import models
from apps.base.models import BaseModel
from apps.users.models import CustomUser
from apps.books.models import Book



class Cart(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


     def __str__(self):
          return f'Cart of {self.user.username}'
     

     def total_price(self):
          return sum(item.total_price() for item in self.items.all())



class CartItem(BaseModel):
     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)

     STATUS_CHOICES = [
     ("pending", "Pending"),
     ("confirmed", "Confirmed"),
     ("shipped", "Shipped"),
     ("delivered", "Delivered"),
     ("cancelled", "Cancelled"),
     ]

     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

     def total_price(self):
          return self.book.price * self.quantity
     
     
     def __str__(self):
          return f"{self.quantity}x {self.book.title} in {self.cart.user.username}'s cart  - {self.status}"



class Order(BaseModel):
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

     STATUS_CHOICES = [
          ("pending", "Pending"),
          ("confirmed", "Confirmed"),
          ("shipped", "Shipped"),
          ("delivered", "Delivered"),
          ("cancelled", "Cancelled"),
     ]

     address = models.TextField()  # 🏠 Yetkazib berish manzili
     phone = models.CharField(max_length=15)  # 📞 Telefon raqami

     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

     PAYMENT_STATUS_CHOICES = [
          ("paid", "Paid"),
          ("failed", "Failed"),
     ]

     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")  # To‘lov statusi

     def __str__(self):
          return f"Order {self.id} by {self.user.username} - {self.status} - {self.payment_status}"



class OrderItem(BaseModel):
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
     book = models.ForeignKey(Book, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField(default=1)
     price = models.DecimalField(max_digits=10, decimal_places=2)

     def __str__(self):
          return f"{self.quantity}x {self.book.title} in Order {self.order.id}"
