from django.urls import path

from .views import *
from . import views
app_name = 'blog'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('news_category/', NewsCategoryList.as_view(), name='news_post_list'),
    path('drafts/', DraftPostList.as_view(), name='draft_post_list'),
    path('entertainment_category/', EntCategoryList.as_view(), name='ent_post_list'),
    path('technology_category/', TechCategoryList.as_view(), name='tech_post_list'),
    path('<int:pk>/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/<slug:slug>/delete/', post_delete, name='post_delete'),
    path('<int:pk>/<slug:slug>/edit', PostUpdate.as_view(), name='post_edit'),
    path('register/', SignUpView.as_view(), name = 'user_register'),
    path('profile/', ProfileView.as_view(), name="user_profile"),
    path('profile_update/', ProfileUpdateView.as_view(), name="profile_update"),
    path('like/', views.like_post, name="like_post"),
    path('favourite/', views.favourite_post, name="favourite_post"),
    path('favourite_post_list/', FavPostList.as_view(), name="favourite_post_list"),
]