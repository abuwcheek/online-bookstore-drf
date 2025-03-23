from django.urls import path

from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
)

urlpatterns = [
     # Token olish uchun
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

     # Tokenni yangilash uchun
     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     ]



from .views import (CustomUserRegisterView, LogInUserView, 
                    LogoutUserView, CustomUserViewProfileView, 
                    CustomUserUpdateView, CustomUserDestroyView)


urlpatterns += [
     path('register-user', CustomUserRegisterView.as_view()),
     path('login-user', LogInUserView.as_view()),
     path('logout-user', LogoutUserView.as_view()),
     path('profile-user', CustomUserViewProfileView.as_view()),
     path('update-user', CustomUserUpdateView.as_view()),
     path('delete-user', CustomUserDestroyView.as_view()),
]