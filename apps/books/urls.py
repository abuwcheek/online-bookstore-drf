from django.urls import path
from .views import CategoryCreateView, CategoryListView, CategoryDestroyView


# Category uchun url
urlpatterns = [
     path('category/create', CategoryCreateView.as_view()),
     path('category/list', CategoryListView.as_view()),
     path('category/delete/<int:pk>', CategoryDestroyView.as_view()),
]




from .views import BookCreateView, BookListView

# book uchun url
urlpatterns += [
     path('book/create', BookCreateView.as_view()),
     path('book/list', BookListView.as_view()),
]