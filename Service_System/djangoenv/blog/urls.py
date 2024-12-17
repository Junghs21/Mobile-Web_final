from django.urls import path
from . import views
from django.urls import include
from rest_framework import routers
from .views import DeletePostAPIView
from .views import PostTitleImageAPIView

router = routers.DefaultRouter()
router.register('Post', views.blogImage)


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api_root/', include(router.urls)),
    path('delete_image/', DeletePostAPIView.as_view(), name='delete_post'),
    path('api_root/titles/', PostTitleImageAPIView.as_view(), name='post_titles'),  # 새로운 엔드포인트
]
