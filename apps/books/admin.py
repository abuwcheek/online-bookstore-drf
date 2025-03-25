from traceback import format_tb
from django.utils.html import format_html
from django.contrib import admin
from .models import Category, Book, BookImage, Wishlist, BookRating, View


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     list_display_links = ('id', 'name')
     search_fields = ('name',)
     list_per_page = 25



class BookImageInline(admin.StackedInline):
     model = BookImage
     extra = 1  # Qo‘shimcha maydon qo‘shish (yangi rasm qo‘shish imkoniyati)
     readonly_fields = ('get_image',)  # Rasmlarni oldindan ko‘rsatish

     def get_image(self, obj):
          if obj.image:
               return format_html('<img src="{}" style="max-height: 150px;"/>', obj.image.url)
          return "-"
          

     get_image.short_description = "Rasm"
     


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
     inlines = [BookImageInline]
     list_display = ('id', 'title', 'author', 'price', 'book_type', 'stock', 'is_published', 'is_featured', 'is_bestseller', 'is_new', 'is_popular', 'is_free', 'is_discount', 'discount_price', 'year_publication', 'is_active')
     list_display_links = ('id', 'title', 'author', 'price',)
     search_fields = ('title', 'author', 'country_origin', 'price', 'is_published', 'is_featured', 'is_bestseller', 'is_new', 'is_popular')
     list_editable = ('is_published', 'is_featured', 'is_bestseller', 'is_new', 'is_popular', 'is_free', 'is_discount', 'is_active')
     readonly_fields = ('views',)
     list_per_page = 25




@admin.register(Wishlist)
class BookLikeAdmin(admin.ModelAdmin):
     list_display = ('id', 'book', 'user', 'created_at')
     list_display_links = ('id', 'book', 'user')
     search_fields = ('book', 'user', 'created_at')
     list_per_page = 25



@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
     list_display = ('id', 'book__id', 'book', 'user', 'rating', 'review', 'created_at')
     list_display_links = ('id', 'book', 'user')
     search_fields = ('book', 'user', 'rating', 'review', 'created_at')
     list_per_page = 25



@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
     list_display = ('id', 'book', 'user', 'created_at')
     list_display_links = ('id', 'book', 'user')
     search_fields = ('book', 'user', 'created_at')
     list_per_page = 25