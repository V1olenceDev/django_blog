from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:username>/',
         views.profile, name='profile'),
    path('edit_profile/<slug:username>/',
         views.EditProfile.as_view(), name='edit_profile'),
    path('posts/create/',
         views.CreatePost.as_view(), name='create_post'),
    path('posts/<int:post_pk>/',
         views.PostDetail.as_view(), name='post_detail'),
    path('posts/<int:post_id>/edit/',
         views.UpdatePost.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.delete_post, name='delete_post'),
    path('category/<slug:category_slug>/',
         views.CategoryPosts.as_view(), name='category_posts'),
    path('posts/<int:post_pk>/comment/',
         views.add_comment, name='add_comment'),
    path('posts/<int:post_pk>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_pk>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
]
