from video_games.models import Developer, Region, Game, GameDeveloper, Genre, Platform, Publisher, Rating, Sale
from rest_framework import response, serializers, status

# Serializer for Developer
class DeveloperSerializer(serializers.ModelSerializer):

	class Meta:
		model = Developer
		fields = ('developer_id', 'developer_name')

# Serializer for Region
class RegionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Region
		fields = ('region_id', 'region_name')

# Serializer for GameDeveloper
class GameDeveloperSerializer(serializers.ModelSerializer):
	game_id = serializers.ReadOnlyField(source='game.game_id')
	developer_id = serializers.ReadOnlyField(source='developer.developer_id')

	class Meta:
		model = GameDeveloper
		fields = ('game_id', 'developer_id')

# Serializer for Genre
class GenreSerializer(serializers.ModelSerializer):

	class Meta:
		model = Genre
		fields = ('genre_id', 'genre_name')

# Serializer for Platform
class PlatformSerializer(serializers.ModelSerializer):

	class Meta:
		model = Platform
		fields = ('platform_id', 'platform_name')

# Serializer for Publisher
class PublisherSerializer(serializers.ModelSerializer):

	class Meta:
		model = Publisher
		fields = ('publisher_id', 'publisher_name')

# Serializer for Rating
class RatingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Rating
		fields = ('rating_id', 'rating_name')

# Serializer for Sale
class SaleSerializer(serializers.ModelSerializer):
	game_id = serializers.ReadOnlyField(source='game.game_id')
	region_id = serializers.ReadOnlyField(source='region.region_id')

	class Meta:
		model = Sale
		fields = ('game_id', 'region_id', 'total_sales')

# Similar to HeritageSiteSerializer from Assignment 10
class GameSerializer(serializers.ModelSerializer):
	game_name = serializers.CharField(
			allow_blank=False,
			max_length=255
	)
	year_released = serializers.IntegerField(
			allow_null=True
	)
	critic_score = serializers.IntegerField(
			allow_null=True
	)
	critic_count = serializers.IntegerField(
			allow_null=True
	)
	user_score = serializers.IntegerField(
			allow_null=True
	)
	user_count = serializers.IntegerField(
			allow_null=True
	)
	# Work through the Foreign key fields
	platform = PlatformSerializer(
			many=False,
			read_only=True
	)
	platform_id = serializers.PrimaryKeyRelatedField(
			allow_null=True,
			many=False,
			write_only=True,
			queryset=Platform.objects.all(),
			source='platform'
	)
	genre = GenreSerializer(
			many=False,
			read_only=True
	)
	genre_id = serializers.PrimaryKeyRelatedField(
			allow_null=True,
			many=False,
			write_only=True,
			queryset=Genre.objects.all(),
			source='genre'
	)
	publisher = PublisherSerializer(
			many=False,
			read_only=True
	)
	publisher_id = serializers.PrimaryKeyRelatedField(
			allow_null=True,
			many=False,
			write_only=True,
			queryset=Publisher.objects.all(),
			source='publisher'
	)
	rating = RatingSerializer(
			many=False,
			read_only=True
	)
	rating_id = serializers.PrimaryKeyRelatedField(
			allow_null=True,
			many=False,
			write_only=True,
			queryset=Rating.objects.all(),
			source='rating'
	)

	# Handle m2m relationships
	game_developer = GameDeveloperSerializer(
			source='game_developer_set',
			many=True,
			read_only=True
	)
	game_dev_ids = serializers.PrimaryKeyRelatedField(
			many=True,
			write_only=True,
			queryset=Developer.objects.all(),
			source='game_developer'
	)
	sale = SaleSerializer(
			source='sale_set',
			many=True,
			read_only=True
	)
	sale_ids = serializers.PrimaryKeyRelatedField(
			many=True,
			write_only=True,
			queryset=Region.objects.all(),
			source='sale'
	)

	class Meta:
		model = Game
		fields = (
				'game_id',
				'game_name',
				'year_released',
				'critic_score',
				'critic_count',
				'user_score',
				'user_count',
				'platform',
				'platform_id',
				'genre',
				'genre_id',
				'publisher',
				'publisher_id',
				'rating',
				'rating_id',
				'game_developer',
				'game_dev_ids',
				'sale',
				'sale_ids'
		)


	def create(self, validated_data):
		'''
		This method persists a new Game instance and adds all related fields to the
		GameDeveloper and Sales tables.
		'''
		#print(validated_data)

		developers = validated_data.pop('game_developer')
		regions = validated_data.pop('sale')
		game = Game.objects.create(**validated_data)

		if developers is not None:
			for developer in developers:
				GameDeveloper.objects.create(
							game_id=game.game_id,
							developer_id=developer.developer_id
				)
		if regions is not None:
			for region in regions:
				Sale.objects.create(
							game_id=game.game_id,
							region_id=region.region_id,
							total_sales=0.00
				)
		return game


	def update(self, instance, validated_data):
		game_id = instance.game_id
		new_developers = validated_data.pop('game_developer')
		new_regions = validated_data.pop('sale')

		instance.game_name = validated_data.get(
				'game_name',
				instance.game_name
		)
		instance.year_released = validated_data.get(
				'year_released',
				instance.year_released
		)
		instance.critic_score = validated_data.get(
				'critic_score',
				instance.critic_score
		)
		instance.critic_count = validated_data.get(
				'critic_count',
				instance.critic_count
		)
		instance.user_score = validated_data.get(
				'user_score',
				instance.user_score
		)
		instance.user_count = validated_data.get(
				'user_count',
				instance.user_count
		)
		instance.platform_id = validated_data.get(
				'platform_id',
				instance.platform_id
		)
		instance.genre_id = validated_data.get(
				'genre_id'
		)
		instance.publisher_id = validated_data.get(
				'publisher_id'
		)
		instance.rating_id = validated_data.get(
				'rating_id'
		)
		instance.save()

		# If any existing developers are not in updated list, delete them
		new_dids = []
		old_dids = GameDeveloper.objects.values_list('developer_id', flat=True).filter(game_id__exact=game_id)

		# Insert new unmatched developer entries
		for developer in new_developers:
			new_did = developer.developer_id
			new_dids.append(new_did)
			if new_id in old_dids:
				continue
			else:
				GameDeveloper.objects.create(game_id=game_id, developer_id=new_did)

		for old_did in old_dids:
			if old_did in new_dids:
				continue
			else:
				GameDeveloper.objects.filter(game_id=game_id, developer_id=old_did).delete()


		# For Regions of an update
		new_rids = []
		old_rids = Sale.objects.values_list('region_id', flat=True).filter(region_id__exact=game_id)

		# Insert new unmatched region entries
		for region in new_regions:
			new_rid = region.region_id
			new_rids.append(new_rid)
			if new_rid in old_rids:
				continue
			else:
				Sale.objects.create(game_id=game_id, region_id=new_rid)

		# Delete old unmatched region entries
		for old_rid in old_rids:
			if old_rid in new_rids:
				continue
			else:
				Sale.objects.filter(game_id=game_id, region_id=old_rid).delete()

		print(instance)
		return instance
