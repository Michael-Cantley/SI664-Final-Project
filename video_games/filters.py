import django_filters
from video_games.models import Developer, Region, Game, Genre, Platform, Publisher, Rating, GameDeveloper, Sale


class GameFilter(django_filters.FilterSet):
	game_name = django_filters.CharFilter(
		field_name='game_name',
		label='Video Game Name',
		lookup_expr='icontains'
	)

	# Additional descriptions
	platform = django_filters.ModelChoiceFilter(
		field_name='platform',
		label='Platform',
		queryset=Platform.objects.all().order_by('platform_name'),
		lookup_expr='exact'
	)

	year_released = django_filters.NumberFilter(
		field_name='year_released',
		label='Year Released',
		lookup_expr = 'exact'
	)

	genre = django_filters.ModelChoiceFilter(
		field_name='genre',
		label='Genre',
		queryset=Genre.objects.all().order_by('genre_name'),
		lookup_expr='exact'
	)

	publisher = django_filters.ModelChoiceFilter(
		field_name='publisher',
		label='Publisher',
		queryset=Publisher.objects.all().order_by('publisher_name'),
		lookup_expr='exact'
	)

	rating = django_filters.ModelChoiceFilter(
		field_name='rating',
		label='Rating',
		queryset=Rating.objects.all().order_by('rating_name'),
		lookup_expr='exact'
	)

	region = django_filters.ModelChoiceFilter(
		field_name='region',
		label='Region',
		queryset=Region.objects.all().order_by('region_name'),
		lookup_expr='exact'
	)

	developer = django_filters.ModelChoiceFilter(
		field_name='developer',
		label='Developer',
		queryset=Developer.objects.all().order_by('developer_name'),
		lookup_expr='exact'
	)


	class Meta:
		model = Game
		# form = SearchForm
		# fields [] is required, even if empty.
		fields = []
