from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, logout, get_user

urlpatterns = [
    path('register/', register, name='auth_register'),
    path('login/', login, name='auth_login'),
    path('logout/', logout, name='auth_logout'),
    path('get-user/', get_user, name='auth_get_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]