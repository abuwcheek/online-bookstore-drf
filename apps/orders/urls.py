from django.urls import path
from .views import (CartRetrieveView, CartItemCreateView, 
                    CartItemDestroyView, CartClearView, 
                    CartStatusUpdateView, CartHistoryAPIView,
                    AdminStatsView, UpdatePaymentStatusView)



# Cart uchun url
urlpatterns = [
     path('orders/cart-retrieve', CartRetrieveView.as_view()),
     path('orders/cart-add', CartItemCreateView.as_view()),
     path('orders/cart-remove/<int:book_id>', CartItemDestroyView.as_view()),
     path('orders/cart/<int:pk>/cancel', CartClearView.as_view()),
     path('orders/cart/<int:pk>/status', CartStatusUpdateView.as_view()),
     path('orders/cart/history', CartHistoryAPIView.as_view()),
     path('stats', AdminStatsView.as_view())
]


from .views import CreateOrderView, UserOrdersView, UpdateOrderStatusView, OrderDeleteView, UpdatePaymentStatusView

# Order uchun url
urlpatterns += [
     path('orders/create/user-product', CreateOrderView.as_view()),
     path("orders/<int:order_id>/update-status", UpdateOrderStatusView.as_view()),
     path("orders/<int:order_id>/update-payment", UpdatePaymentStatusView.as_view()),
     path('orders/my-orders', UserOrdersView.as_view()),
     path('orders/<int:order_id>/update-status', UpdateOrderStatusView.as_view()),
     path('orders/<int:order_id>/delete', OrderDeleteView.as_view()),
]