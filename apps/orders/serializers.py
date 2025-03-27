from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from apps.users.models import CustomUser



class CartItemSerializers(serializers.ModelSerializer):
     book_title = serializers.CharField(source='book.title', read_only=True)
     total_price = serializers.SerializerMethodField()

     class Meta:
          model = CartItem
          fields = ['id', 'book', 'book_title', 'quantity', 'total_price', 'status', 'created_at']


     @staticmethod
     def get_total_price(obj):
          return obj.total_price()



class CartSerializers(serializers.ModelSerializer):
     items = CartItemSerializers(many=True, read_only=True)
     total_price = serializers.SerializerMethodField()
     username = serializers.SerializerMethodField()
     count = serializers.SerializerMethodField()

     class Meta:
          model = Cart
          fields = ['count', 'id', 'user', 'username', 'items', 'total_price']

     
     @staticmethod
     def get_total_price(obj):
          return obj.total_price()
     

     @staticmethod
     def get_username(obj):
          return obj.user.username
     
     
     def get_count(self, obj):
          return obj.items.count()




class CartStatusUpdateSerializers(serializers.ModelSerializer):
     class Meta:
          model = CartItem
          fields = ['status']


     def update(self, instance, validated_data):
          instance.status = validated_data.get('status', instance.status)
          instance.save()
          return instance



class OrderItemSerializer(serializers.ModelSerializer):
     class Meta:
          model = OrderItem
          fields = ["book", "quantity", "price"]



class OrderSerializer(serializers.ModelSerializer):
     items = OrderItemSerializer(many=True, read_only=True)  # Buyurtmadagi mahsulotlarni qo'shish

     class Meta:
          model = Order
          fields = ["id", "user", "total_price", "status", "payment_status", "address", "phone", "items"]