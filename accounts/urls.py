from django.urls import path
from .views import LoginView, SignUpView, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('logout', logout_view, name='logout'),
]
