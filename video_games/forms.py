from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import FormActions
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


# class DeveloperForm(forms.ModelForm):
# 	class Meta:
# 		model = Developer
# 		fields = '__all__'
#
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.helper = FormHelper()
# 		self.helper.form_method = 'post'
# 		self.helper.add_input(Submit('submit', 'submit'))


class DeveloperForm(forms.ModelForm):
	developer_name = forms.CharField(label=('Developer'))
	games = forms.ModelMultipleChoiceField(label=('Games'),
										  widget=forms.SelectMultiple(),
										  required=True,
										  queryset=Game.objects.all())
	class Meta:
		model = Developer
		fields = ['developer_name', 'games']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'submit'))
		self.helper.layout = Layout(
			Field('developer_name'),
			Field('games'),
			FormActions(
				Submit('submit', ('Submit'), css_class="btn-primary")
			)
		)
