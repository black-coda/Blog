from django.urls import path
from .views import PostDetailView, PostListView, list_view, authorForm, PostdetailView, list_view, detail_view
from django.conf import settings

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='PostList'),
    path('<int:pk>/', detail_view, name='PostDetail'),
]