from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:id>/', views.article_det, name='article_det'),
    path('api/posts/', views.posts_list),
    path('api/posts/<int:id>/', views.post_detail),
    path('api/login/', views.login_api),
]