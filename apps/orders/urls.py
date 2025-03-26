from django.urls import path
from .views import CartRetrieveView, CartItemCreateView, CartItemDestroyView, CartClearView, CartStatusUpdateView, CartHistoryAPIView




urlpatterns = [
     path('cart-retrieve', CartRetrieveView.as_view()),
     path('cart-add', CartItemCreateView.as_view()),
     path('cart-remove/<int:book_id>', CartItemDestroyView.as_view()),
     path('cart/<int:pk>/cancel', CartClearView.as_view()),
     path('cart/<int:pk>/status', CartStatusUpdateView.as_view()),
     path('cart/history', CartHistoryAPIView.as_view()),
]