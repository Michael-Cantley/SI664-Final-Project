from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from video_games.models import Game, Sale, Region, Developer, GameDeveloper


class GameForm(forms.ModelForm):
	class Meta:
		model = Game
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))


class DeveloperForm(forms.ModelForm):
	class Meta:
		model = Developer
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))
