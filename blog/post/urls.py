from django.urls import path
from . import views


urlpatterns = [
   path('', views.all_posts, name='all-posts'),
   path('add-post/', views.add_post, name='add-post'),
   path('update-post/<int:pk>/', views.update_post, name='update-post'),
   path('post-details/<int:pk>/', views.post_details, name='post-details'),
   path('author-posts/<int:pk>/', views.author_posts, name='author-posts'),
   path('my-posts/', views.my_posts, name='my-posts'),
   path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
   path('like-post/<int:pk>/', views.like_post, name='like-post'),
#    path('draft-posts/', views.draft_posts, name='draft-posts'),

]