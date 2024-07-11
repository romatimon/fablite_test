from django.urls import path
from user.views import UserView, login

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('users/<int:user_id>/', UserView.as_view(), name='user_detail'),
    path('login/', login, name='login'),
]