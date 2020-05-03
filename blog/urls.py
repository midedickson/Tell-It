from django.urls import path

from .views import PostList, PostCreate, SignUpView, ProfileView, ProfileUpdateView, post_delete, PostUpdate, PostDetail
from . import views
app_name = 'blog'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/<slug:slug>/delete/', post_delete, name='post_delete'),
    path('<int:pk>/<slug:slug>/edit', PostUpdate.as_view(), name='post_edit'),
    path('register/', SignUpView.as_view(), name = 'user_register'),
    path('profile/', ProfileView.as_view(), name="user_profile"),
    path('profile_update/', ProfileUpdateView.as_view(), name="profile_update"),
    path('like/', views.like_post, name="like_post"),
]