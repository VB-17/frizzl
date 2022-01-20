from .views import HomeView, follow_user_view, user_profile_view
from django.urls import path


app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('user/<str:username>/', user_profile_view, name='profile'),
    path('follow/user', follow_user_view, name='follow-user')
]
