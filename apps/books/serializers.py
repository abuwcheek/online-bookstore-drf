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

