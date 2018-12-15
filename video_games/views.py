from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Game


def index(request):
	return HttpResponse("Hello, world. You're at the Video Games Sales index.")


class AboutPageView(generic.TemplateView):
	template_name = 'video_games/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'video_games/home.html'


class GameListView(generic.ListView):
	model = Game
	context_object_name = 'games'
	template_name = 'video_games/games.html'
	paginate_by = 50

	def get_queryset(self):
		return Game.objects.all().select_related('platform', 'genre', 'publisher', 'rating').order_by('game_name')

class GameDetailView(generic.DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'video_games/game_detail.html'
