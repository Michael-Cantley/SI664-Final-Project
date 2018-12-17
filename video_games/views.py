from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Game, Sale
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Added for assignment #8
from .forms import GameForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Sale, GameDeveloper, Developer
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# Assignment 9
from .filters import GameFilter
from django_filters.views import FilterView


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
	paginate_by = 500

	def get_queryset(self):
		return Game.objects.all().select_related('platform', 'genre', 'publisher', 'rating').order_by('game_name')

class GameDetailView(generic.DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'video_games/game_detail.html'


@method_decorator(login_required, name='dispatch')
class SaleListView(generic.ListView):
	model = Sale
	context_object_name = 'sales'
	template_name = 'video_games/sales.html'
	paginate_by = 2000

	def get_queryset(self):
		return Sale.objects.select_related('game', 'region').order_by('total_sales')

@method_decorator(login_required, name='dispatch')
class SaleDetailView(generic.DetailView):
	model = Sale
	context_object_name = 'sale'
	template_name = 'video_games/sale_detail.html'

# For Game Create View - Assignment #8
@method_decorator(login_required, name='dispatch')
class GameCreateView(generic.View):
    model = Game
    form_class = GameForm
    success_message = "New Game created successfully"
    template_name = 'video_games/game_new.html'
    # fields = '__all__' <-- superseded by form_class
    # success_url = reverse_lazy('heritagesites/site_list')

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.save()
            for developer in form.cleaned_data['developer']:
                GameDeveloper.objects.create(game=game, developer=developer)
            for region in form.cleaned_data['region']:
                Sale.objects.create(game=game, region=region, total_sales=0.00)
            return redirect(game) # shortcut to object's get_absolute_url()
            # return HttpResponseRedirect(site.get_absolute_url())
        return render(request, 'video_games/game_new.html', {'form': form})

    def get(self, request):
        form = GameForm()
        return render(request, 'video_games/game_new.html', {'form': form})

# Updating the View for a Game- assignment#8
@method_decorator(login_required, name='dispatch')
class GameUpdateView(generic.UpdateView):
    model = Game
    form_class = GameForm
    # fields = '__all__' <-- superseded by form_class
    context_object_name = 'game'
    # pk_url_kwarg = 'site_pk'
    success_message = "The video game updated successfully"
    template_name = 'video_games/game_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        game = form.save(commit=False)
        # site.updated_by = self.request.user
        # site.date_updated = timezone.now()
        game.save()

        # Current country_area_id values linked to site
        old_ids = GameDeveloper.objects.values_list('developer_id', flat=True).filter(game_id=game.game_id)

        # New countries list
        new_developers = form.cleaned_data['developer']

        # New ids
        new_ids = []

        # Insert new unmatched country entries
        for developer in new_developers:
            new_id = developer.developer_id
            new_ids.append(new_id)
            if new_id in old_ids:
                continue
            else:
                GameDeveloper.objects.create(game=game, developer=developer)

        # Delete old unmatched country entries
        for old_id in old_ids:
            if old_id in new_ids:
                continue
            else:
                GameDeveloper.objects.filter(game_id=game.game_id, developer_id=old_id).delete()

        old_sids = Sale.objects.values_list('region_id', flat=True).filter(game_id=game.game_id)
        # New Regions list
        new_regions = form.cleaned_data['region']

        # New SIDS
        new_sids=[]

        # Insert new unmatched region entries
        for region in new_regions:
            new_sid = region.region_id
            new_sids.append(new_sid)
            if new_sid in old_sids:
                continue
            else:
                Sale.objects.create(game=game, region=region, total_sales=0.00)

        #Delete old unmatched region entries
        for old_sid in old_sids:
            if old_sid in new_sids:
                continue
            else:
                Sale.objects.filter(game_id=game.game_id, region_id=old_sid).delete()



        return HttpResponseRedirect(game.get_absolute_url())
        #return redirect('heritagesites/site_detail', pk=site.pk)

@method_decorator(login_required, name='dispatch')
class GameDeleteView(generic.DeleteView):
    model = Game
    success_message = "Video Game deleted successfully"
    success_url = reverse_lazy('games') # Adjusted to match appropriate "sites"
    context_object_name = 'game'
    template_name = 'video_games/game_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete GameDeveloper entries
        GameDeveloper.objects.filter(game_id=self.object.game_id).delete()

        # Delete Sale entries
        Sale.objects.filter(game_id=self.object.game_id).delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

class GameFilterView(FilterView):
    filterset_class = GameFilter
    template_name = 'video_games/game_filter.html'
