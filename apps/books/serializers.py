from rest_framework import serializers
from .models import Category, Book, BookImage, BookRating, BookLike




class CategorySerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['name']



class CategoryListSerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'name', 'created_at',]



class BookCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = Book
          fields = ['title', 'category', 'description', 'weight', 
                    'internal_number', 'book_language', 'written_language', 
                    'translator', 'book_pages', 'book_cover', 'book_type', 
                    'file', 'stock', 'year_publication', 'country_origin', 'price',]
          
     
     def validate(self, attrs):
          if attrs['price'] < 0:
               raise serializers.ValidationError("Narxi manfiy bo'lishi mumkin emas")
          
          if attrs['internal_number'] < 0:
               raise serializers.ValidationError("Ichki raqam manfiy bo'lishi mumkin emas")
          
          if attrs['book_pages'] < 0:
               raise serializers.ValidationError("Sahifalar soni manfiy bo'lishi mumkin emas")
          
          return attrs