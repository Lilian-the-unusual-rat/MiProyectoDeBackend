from django.urls import path
from . import api_views

urlpatterns = [
    path('posts/', api_views.posts_list, name='api_posts_list'),            # GET, POST
    path('posts/<int:id>/', api_views.post_detail, name='api_post_detail'), # GET, PUT/PATCH, DELETE
]