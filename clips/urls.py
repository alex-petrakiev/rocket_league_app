from django.urls import path
from . import views

app_name = 'clips'

urlpatterns = [
    path('', views.ClipListView.as_view(), name='list'),
    path('<int:pk>/', views.ClipDetailView.as_view(), name='detail'),
    path('upload/', views.clip_upload_view, name='upload'),
    path('<int:pk>/rate/', views.rate_clip_view, name='rate'),
]