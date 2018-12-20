from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Game, Sale, Developer, GameDeveloper
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Added for assignment #8
from .forms import GameForm, DeveloperForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Sale, GameDeveloper, Developer, Region
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

class PaginatedFilterView(generic.View):
    """
    Creates a view mixin, which separates out default 'page' keyword and returns the
    remaining querystring as a new template context variable.
    https://stackoverflow.com/questions/51389848/how-can-i-use-pagination-with-django-filter
    """
    def get_context_data(self, **kwargs):
        context = super(PaginatedFilterView, self).get_context_data(**kwargs)
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            context['querystring'] = querystring.urlencode()
        return context

class GameFilterView(PaginatedFilterView, FilterView):
    model = Game
    filterset_class = GameFilter
    context_object_name = 'game_list'
    template_name = 'video_games/game_filter.html'
    paginate_by = 30


# For Extra Credit making CRUD for Developers
class DeveloperListView(generic.ListView):
    model = Developer
    context_object_name = 'developers'
    template_name = 'video_games/developers.html'
    paginate_by = 100

    def get_queryset(self):
        return Developer.objects.all().order_by('developer_name')

class DeveloperDetailView(generic.DetailView):
	model = Developer
	context_object_name = 'developer'
	template_name = 'video_games/developer_detail.html'

@method_decorator(login_required, name='dispatch')
class DeveloperCreateView(generic.View):
    model = Developer
    form_class = DeveloperForm
    success_message = "Developer created successfully"
    template_name = 'video_games/developer_new.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        form = DeveloperForm(request.POST)
        if form.is_valid():
            developer = form.save(commit=False)
            developer.save()
            Developer.objects.create(developer=developer)
            # for game in form.cleaned_data['game']:
            #     GameDeveloper.objects.create(developer=developer, game=game)
            return redirect(developer)
        return render(request, 'video_games/developer_new.html', {'form': form})

    def get(self, request):
        form = DeveloperForm()
        return render(request, 'video_games/developer_new.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeveloperUpdateView(generic.UpdateView):
    model = Developer
    form_class = DeveloperForm
    context_object_name = 'developer'
    success_message = "Developer Record Updated succesfully"
    template_name = 'video_games/developer_update.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        developer = form.save(commit=False)
        developer.save()
        old_devids = Developer.objects.filter(developer_id=developer.developer_id)

        # New developers list
        new_devs = form.cleaned_data['developer']

        new_devids = []




        old_gids = GameDeveloper.objects.values_list('game_id', flat=True).filter(developer_id=developer.developer_id)

        # New games list
        new_games = form.cleaned_data['game']

        # New game ids (gids)
        new_gids = []

        # Insert new unmatched game entries
        for game in new_games:
            new_gid = game.game_id
            new_gids.append(new_gid)
            if new_gid in old_gids:
                continue
            else:
                GameDeveloper.objects.create(developer=developer, game=game)

        # Delete old unmatched game entries
        for old_gid in old_gids:
            if old_gid in new_gids:
                continue
            else:
                GameDeveloper.objects.filter(developer_id=developer.developer_id, game_id=old_gid).delete()

        return HttpResponseRedirect(developer.get_absolute_url())

@method_decorator(login_required, name='dispatch')
class DeveloperDeleteView(generic.DeleteView):
    model = Developer
    success_message = "Developer deleted succesfully"
    success_url = reverse_lazy('developers')
    context_object_name = 'developer'
    template_name = 'video_games/developer_delete.html'

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete GameDeveloper entries
        GameDeveloper.objects.filter(developer_id=self.object.developer_id).delete()

        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())
