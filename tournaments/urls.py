from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.TournamentListView.as_view(), name='list'),
    path('<int:pk>/', views.TournamentDetailView.as_view(), name='detail'),
    path('create/', views.tournament_create_view, name='create'),
    path('<int:pk>/join/', views.join_tournament_view, name='join'),
]