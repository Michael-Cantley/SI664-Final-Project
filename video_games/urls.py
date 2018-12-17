from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('sales/', views.SaleListView.as_view(), name='sales'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale_detail'),
    # From assignment #8
    path('games/new/', views.GameCreateView.as_view(), name='game_new'),
    path('games/<int:pk>/delete/', views.GameDeleteView.as_view(), name='game_delete'),
    path('games/<int:pk>/update/', views.GameUpdateView.as_view(), name='game_update'),
]


# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#    path('', views.index, name='index'),
# ]
