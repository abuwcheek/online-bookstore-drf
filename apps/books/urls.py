from django.urls import path
from .views import CategoryCreateView, CategoryListView, CategoryDestroyView


# Category ga url qo'shish
urlpatterns = [
     path('category/create', CategoryCreateView.as_view()),
     path('category/list', CategoryListView.as_view()),
     path('category/delete/<int:pk>', CategoryDestroyView.as_view()),
]