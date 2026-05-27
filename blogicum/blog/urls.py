from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/logout/', views.custom_logout, name='logout'),

    path('posts/create/', views.create, name='create_post'),
    path('posts/<int:post_id>/', views.detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.edit, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete, name='delete_post'),

    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>',
        views.delete_comment, name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment, name='edit_comment'
    ),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),

    path(
        'category/<slug:category_slug>/',
        views.category, name='category_posts'
    ),

    path('profile/<slug:username_slug>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile')
]
