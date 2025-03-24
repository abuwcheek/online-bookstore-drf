from rest_framework import serializers
from .models import Category, Book, BookImage, BookRating, BookLike




class CategoryCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['name']



class CategoryListSerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'name', 'created_at',]



class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'name']



class BookCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = Book
          fields = ['title', 'author', 'category', 'description', 'weight', 
                    'internal_number', 'book_language', 'written_language', 
                    'translator', 'book_pages', 'book_cover', 'book_type', 
                    'file', 'stock', 'year_publication', 'country_origin', 'price', 'discount_price']
          
     
     def validate(self, attrs):
          if attrs['price'] < 0:
               raise serializers.ValidationError("Narxi manfiy bo'lishi mumkin emas")
          
          if attrs['internal_number'] < 0:
               raise serializers.ValidationError("Ichki raqam manfiy bo'lishi mumkin emas")
          
          if attrs['book_pages'] < 0:
               raise serializers.ValidationError("Sahifalar soni manfiy bo'lishi mumkin emas")
          
          if attrs['discount_price'] < 0:
               raise serializers.ValidationError("Chegirma 0 dan kichik bo'lishi mumkin emas")
          
          return attrs



class BookListSerializer(serializers.ModelSerializer):
     discounted_price = serializers.SerializerMethodField()
     rating = serializers.SerializerMethodField()
     category = CategorySerializer()
     image = serializers.SerializerMethodField()
     class Meta:
          model = Book
          fields = ['id', 'image', 'title', 'category', 'author', 'discounted_price', 'rating']


     @staticmethod
     def get_discounted_price( obj):
          return obj.final_price


     def get_rating(self, obj):
          return obj.average_rating


     
     def get_image(self, obj):
          request = self.context.get("request")  # Request objectni olish
          main_image = obj.images.filter(is_main=True).first()
          if main_image:
               return request.build_absolute_uri(main_image.image.url)  # To‘liq URL yaratish
          return None  # Agar asosiy rasm bo‘lmasa, `None` qaytariladi
