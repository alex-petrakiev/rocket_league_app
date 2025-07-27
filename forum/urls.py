from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.ForumPostListView.as_view(), name='list'),
    path('<int:pk>/', views.ForumPostDetailView.as_view(), name='detail'),
    path('create/', views.forum_post_create_view, name='create'),
    path('<int:pk>/comment/', views.add_comment_view, name='add_comment'),
]