from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('games/', views.GameListView.as_view(), name='games'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
]


# from django.urls import path
#
# from . import views
#
# urlpatterns = [
#    path('', views.index, name='index'),
# ]
