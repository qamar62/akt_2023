from django.urls import path
from . import views
from .views import Blogs, BlogDetailView, AddPostView, UpdatePostView, DeletePostView, AddCommentView


urlpatterns = [
    path('', Blogs.as_view(), name = "blogs"),
    path('article/<int:pk>/', BlogDetailView.as_view(), name = "blog-detail"),
    path('add_post/', AddPostView.as_view(), name = "add-post"),
    path('article/edit/<int:pk>/', UpdatePostView.as_view(), name = "update-post"),
    path('article/<int:pk>/remove', DeletePostView.as_view(), name = "delete-post"),
   
    path('article/<int:pk>/comment/', AddCommentView.as_view(), name="add-comment"),
    path('likes/', views.like_post, name='like_post'),
]
