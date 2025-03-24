from django.db import models
from apps.base.models import BaseModel
from apps.users.models import CustomUser



class Category(BaseModel):
     name = models.CharField(max_length=255)

     def __str__(self):
          return self.name
     


class Book(BaseModel):
     title = models.CharField(max_length=255)
     author = models.CharField(max_length=255, null=True, blank=True)
     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
     description = models.TextField(verbose_name="Kitob haqida", null=True, blank=True)
     weight = models.IntegerField(verbose_name="Og'irligi")
     internal_number = models.IntegerField(verbose_name="Ichki raqam")
     book_language = models.CharField(max_length=255, verbose_name="Kitob tili")
     written_language = models.CharField(max_length=255, verbose_name="Yozilgan tili")
     translator = models.CharField(max_length=255, verbose_name="Kim tarjima qigani", null=True, blank=True)
     book_pages = models.IntegerField(verbose_name="Sahifalar soni")
     book_cover = models.CharField(max_length=255, verbose_name="Kitob muqovasi")

     BOOK_TYPE_CHOICES = (
          ('elektron', 'Elektron'), 
          ('bosma', 'Bosma')
          )
     book_type = models.CharField(max_length=10, choices=BOOK_TYPE_CHOICES, default='bosma', verbose_name="Kitob turi")
     # Kitob fayli (PDF, EPUB) – onlayn yuklab olish uchun
     file = models.FileField(upload_to="books/", verbose_name="Kitob fayli", null=True, blank=True)
     stock = models.IntegerField(default=0, verbose_name="Ombordagi soni", null=True, blank=True)

     year_publication = models.IntegerField(verbose_name="Nashr yili")
     # Kutubxona yoki do‘kon joylashuvi
     country_origin = models.CharField(max_length=255, verbose_name="Nashr Mamlakati")
     price = models.IntegerField(verbose_name="Narxi")

     views = models.IntegerField(default=0, verbose_name="Ko‘rishlar soni")
     
     discount_price = models.IntegerField(default=0, verbose_name="Chegirma narxi", null=True, blank=True)
     is_discount = models.BooleanField(default=False, verbose_name="Chegirma bor yoki yo'q")
     is_free = models.BooleanField(default=False, verbose_name="Bepulmi yoki yo'q")
     is_published = models.BooleanField(default=False, verbose_name="Nashr qilinganmi yoki yo'q")
     is_featured = models.BooleanField(default=False, verbose_name="Taniqli kitobmi yoki yo'q")
     is_bestseller = models.BooleanField(default=False, verbose_name="Eng ko'p sotilgan kitobmi yoki yo'q")
     is_new = models.BooleanField(default=False, verbose_name="Yangimi yoki yo'q")
     is_popular = models.BooleanField(default=False, verbose_name="Ommabopmi yoki yo'q")
     is_top_rated = models.BooleanField(default=False, verbose_name="Eng yaxshi reytingga ega kitobmi yoki yo'q")



     @property
     def final_price(self):
          if self.discount_price:  
               return self.price * (1 - self.discount_price / 100)  # Chegirmali narx
          return self.price  # Asl narx


     @property
     def average_rating(self):
          return self.ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0


     def __str__(self):
          return f'{self.title} - {self.author}'
     


class BookImage(BaseModel):
     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
     image = models.ImageField(upload_to="books/images/")
     is_main = models.BooleanField(default=False)


     def __str__(self):
          return f"{self.book.title} rasmi"


class BookRating(BaseModel):
     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     review = models.TextField(null=True, blank=True)

     choices = (
     (1, 1),
     (2, 2),
     (3, 3),
     (4, 4),
     (5, 5)
     )
     rating = models.PositiveIntegerField(choices=choices, null=True, blank=True)



     def __str__(self):
          return f"{self.user.username} → {self.book.title} ({self.rating})"



class BookLike(BaseModel):
     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='boo_likes')
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

     def __str__(self):
          return f"{self.user.username} → {self.book.title}"