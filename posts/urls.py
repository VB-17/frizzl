from django.urls import path
from .views import PostDetailView, post_delete_view, post_like_view, comment_like_view

app_name = 'posts'

urlpatterns = [
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('<int:pk>/delete', post_delete_view, name='delete'),
    path('post/like', post_like_view, name='like'),
    path('comment/like', comment_like_view, name='comment-like' )
]
