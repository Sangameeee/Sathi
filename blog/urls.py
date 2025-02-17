from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/', views.user_posts, name='user-posts'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:post_id>/update/', views.update_post, name='post-update'),
    path('post/<int:post_id>/delete/', views.delete_post, name='post-delete'),
    path('about/', views.about, name='about')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)