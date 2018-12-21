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
    # Assignment #9
    path('games/search', views.GameFilterView.as_view(), name="search"),
    # Extra Credit
    path('developers/', views.DeveloperListView.as_view(), name='developers'),
    path('developers/<int:pk>/', views.DeveloperDetailView.as_view(), name='developer_detail'),
    path('developers/new/', views.DeveloperCreateView.as_view(), name='developer_new'),
    path('developers/<int:pk>/delete/', views.DeveloperDeleteView.as_view(), name='developer_delete'),
    path('developers/<int:pk>/update/', views.DeveloperUpdateView.as_view(), name='developer_update'),
]


# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#    path('', views.index,  name='index'),
# ]
