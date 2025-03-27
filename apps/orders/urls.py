from django.urls import path
from .views import (CartRetrieveView, CartItemCreateView, 
                    CartItemDestroyView, CartClearView, 
                    CartStatusUpdateView, CartHistoryAPIView,
                    AdminStatsView)




urlpatterns = [
     path('orders/cart-retrieve', CartRetrieveView.as_view()),
     path('orders/cart-add', CartItemCreateView.as_view()),
     path('orders/cart-remove/<int:book_id>', CartItemDestroyView.as_view()),
     path('orders/cart/<int:pk>/cancel', CartClearView.as_view()),
     path('orders/cart/<int:pk>/status', CartStatusUpdateView.as_view()),
     path('orders/cart/history', CartHistoryAPIView.as_view()),
     path('stats', AdminStatsView.as_view())
]



