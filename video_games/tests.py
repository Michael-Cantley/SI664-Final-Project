from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from .models import Game, Platform, Genre, Publisher, Rating


class IndexViewTest(TestCase):

	def test_view_route_redirection(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 302)


class HomeViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/video_games/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_name(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('home'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'video_games/home.html')


class AboutViewTest(TestCase):

	def test_view_route(self):
		response = self.client.get('/video_games/about/')
		self.assertEqual(response.status_code, 200)

	def test_view_route_fail(self):
		response = self.client.get('/about/')
		self.assertEqual(response.status_code, 404)

	def test_view_route_name(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)

	def test_view_template(self):
		response = self.client.get(reverse('about'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'video_games/about.html')

# https://stackoverflow.com/questions/17813919/django-error-matching-query-does-not-exist/30698861
class GameModelTest(TestCase):

    def setUp(self):
        Platform.objects.create(platform_name='Wii')
        platform = Platform.objects.get(pk=27)
        Genre.objects.create(genre_name='Sports')
        genre = Genre.objects.get(pk=11)
        Publisher.objects.create(publisher_name='Nintendo')
        publisher = Publisher.objects.get(pk=362)
        Rating.objects.create(rating_name='E')
        rating = Rating.objects.get(pk=2)
        Game.objects.create(
            game_id=1,
            game_name='Wii Sports',
            platform_id=27,
            year_released=2006,
            genre_id=11,
            publisher_id=362,
            critic_score=76,
            critic_count=51,
            user_score=8,
            user_count=322,
            rating_id=2)

    def test_site_name(self):
        game = Game.objects.get(pk=1)
        expected_object_name = f'{game.game_name}'
        self.assertEqual(expected_object_name, 'Wii Sports')

class GameListViewTest(TestCase):

    def test_view_route(self):
        response = self.client.get('/video_games/games/')
        self.assertEqual(response.status_code, 200)

    def test_view_route_fail(self):
        response = self.client.get('/games/')
        self.assertEqual(response.status_code, 404)

    def test_view_route_name(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)

    def test_view_template(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_games/games.html')
