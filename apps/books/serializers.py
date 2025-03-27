from rest_framework import serializers
from .models import Category, Book, BookImage, BookRating, Wishlist
from apps.orders.models import CartItem



class CategoryCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = Category
          fields = ['id', 'name']



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
          fields = ['id' ,'title', 'author', 'category', 'description', 'weight', 
                    'internal_number', 'book_language', 'written_language', 
                    'translator', 'book_pages', 'book_cover', 'book_type', 
                    'file', 'stock', 'year_publication', 'country_origin', 'price', 'discount_price']
          
     
     def validate_price(self, value):
          if value is None:
               raise serializers.ValidationError("Narxi bo'sh bo'lmasligi kerak")
          if value < 0:
               raise serializers.ValidationError("Narxi manfiy bo'lishi mumkin emas")
          return value
     
     def validate_internal_number(self, value):
          if Book.objects.filter(internal_number=value).exists():
               raise serializers.ValidationError("Bu ichki raqam orqali oldin kitob qo'shilgan")

          if value is None:
               raise serializers.ValidationError("Ichki raqami bo'sh bo'lmasligi kerak")
          if value < 0:
               raise serializers.ValidationError("Ichki raqami manfiy bo'lishi mumkin emas")
          return value



class BookListSerializer(serializers.ModelSerializer):
     new_price = serializers.SerializerMethodField()
     rating = serializers.SerializerMethodField()
     category = CategorySerializer()
     image = serializers.SerializerMethodField()
     is_wishlist = serializers.SerializerMethodField()
     is_cart = serializers.SerializerMethodField()
     class Meta:
          model = Book
          fields = ['id', 'image', 'title', 'category', 'author', 'new_price', 'rating', 'is_wishlist', 'is_cart']


     @staticmethod
     def get_new_price( obj):
          return obj.final_price


     def get_rating(self, obj):
          return obj.average_rating


     def get_image(self, obj):
          request = self.context.get("request")  # Request objectni olish
          main_image = obj.images.filter(is_main=True).first()
          if main_image:
               return request.build_absolute_uri(main_image.image.url)  # To‘liq URL yaratish
          return None  # Agar asosiy rasm bo‘lmasa, `None` qaytariladi


     def get_is_wishlist(self, obj):
          user = self.context['request'].user
          if user.is_authenticated:
               return Wishlist.objects.filter(user=user, book=obj).exists()
          return False
     

     def get_is_cart(self, obj):
          user = self.context['request'].user
          if user.is_authenticated:
               return CartItem.objects.filter(cart__user=user, book=obj).exists()
          return False


class BookUpdateSerializers(serializers.ModelSerializer):
     class Meta:
          model = Book
          fields = ['title', 'author', 'category', 'description', 'weight', 
                    'internal_number', 'book_language', 'written_language', 
                    'translator', 'book_pages', 'book_cover', 'book_type', 
                    'file', 'stock', 'year_publication', 'country_origin', 'price', 'discount_price']



class BookRetrieveSerializers(serializers.ModelSerializer):
     category = CategorySerializer()
     new_price = serializers.SerializerMethodField()
     rating = serializers.SerializerMethodField()
     review = serializers.SerializerMethodField()
     images = serializers.SerializerMethodField()
     views = serializers.SerializerMethodField()

     class Meta:
          model = Book
          fields = ['id', 'images', 'title', 'author', 'category', 'description', 'weight', 
                    'internal_number', 'book_language', 'written_language', 
                    'translator', 'book_pages', 'book_cover', 'book_type', 
                    'file', 'stock', 'year_publication', 'country_origin', 'price', 'new_price', 'views', 'rating', 'review']
          

     @staticmethod
     def get_new_price(obj):
          return obj.final_price
     

     @staticmethod
     def get_rating(obj):
          return obj.average_rating
     

     @staticmethod
     def get_review(obj):
          reviews = obj.ratings.all()
          return BookReviewAddSerializer(reviews, many=True).data
     
     
     def get_images(self, obj):
          request = self.context.get("request")
          images = obj.images.all()
          return [request.build_absolute_uri(image.image.url) for image in images]
     
     def get_views(self, obj):
          return obj.views.count()



class UserAddWishlistSerializer(serializers.ModelSerializer):
     book = BookListSerializer()
     class Meta:
          model = Wishlist
          fields = ['book']



class UserWishlistSerializer(serializers.ModelSerializer):
     book = BookListSerializer()
     count = serializers.SerializerMethodField()
     class Meta:
          model = Wishlist
          fields = ['count' ,'book', 'created_at']


     def get_count(self, obj):
          user = self.context.get("request").user
          return Wishlist.objects.filter(user=user).count()



class BookReviewAddSerializer(serializers.ModelSerializer):
     user = serializers.HiddenField(default=serializers.CurrentUserDefault())
     class Meta:
          model = BookRating
          fields = ['id', 'user', 'book', 'review', 'rating']



class BookReviewUpdateSerializer(serializers.ModelSerializer):
     class Meta:
          model = BookRating
          fields = ['review', 'rating']



class BookReviewListSerializer(serializers.ModelSerializer):
     user = serializers.SerializerMethodField()
     class Meta:
          model = BookRating
          fields = ['id', 'user', 'review', 'rating', 'created_at']


     @staticmethod
     def get_user(obj):
          return obj.user.username
     


class BookTopRatingSerializers(serializers.ModelSerializer):
     rating = serializers.SerializerMethodField()
     class Meta:
          model = Book
          fields = ['id', 'title', 'author', 'rating']


     def get_rating(self, obj):
          return obj.average_rating