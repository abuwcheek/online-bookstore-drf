from django.urls import path
from .views import CategoryCreateView, CategoryListView, CategoryDestroyView



# Category uchun url
urlpatterns = [
     path('category/create', CategoryCreateView.as_view()),
     path('category/list', CategoryListView.as_view()),
     path('category/delete/<int:pk>', CategoryDestroyView.as_view()),
]



from .views import BookCreateView, BookListView, BookUpdateView, BookDestroyView, BookRetrieveView

# book uchun url
urlpatterns += [
     path('book/create', BookCreateView.as_view()),
     path('book/list', BookListView.as_view()),
     path('book/update/<int:pk>', BookUpdateView.as_view()),
     path('book/destroy/<int:pk>', BookDestroyView.as_view()),
     path('book/retrieve/<int:pk>', BookRetrieveView.as_view()),
]



from .views import UserCreateWishlistView, UserWishlistListView, UserDestoryWishlistView

# UserWishlist uchun url
urlpatterns += [
     path('user/wishlist/add-book', UserCreateWishlistView.as_view()),
     path('user/wishlist/list', UserWishlistListView.as_view()),
     path('user/wishlist/delete/<int:pk>', UserDestoryWishlistView.as_view()),
]


from .views import BookReviewAddView, BookReviewUpdateView, BookReviewDestroyView, BookReviewListView, BookTopRatingListView

# BookReview uchun url
urlpatterns += [
     path('book/review/add', BookReviewAddView.as_view()),
     path('book/review/update/<int:pk>', BookReviewUpdateView.as_view()),
     path('book/review/delete/<int:pk>', BookReviewDestroyView.as_view()),
     path('book/review/list/<int:pk>', BookReviewListView.as_view()),
     path('book/top-rating', BookTopRatingListView.as_view()),
]