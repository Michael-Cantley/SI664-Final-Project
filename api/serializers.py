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

		print(validated_data)

	def update(self, instance, validated_data):
		game_id = instance.game_id


# 
# CountryArea, DevStatus, HeritageSite, HeritageSiteCategory, \
# 	HeritageSiteJurisdiction, Location, Planet, Region, SubRegion, IntermediateRegion
# from rest_framework import response, serializers, status
#
#
# class PlanetSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = Planet
# 		fields = ('planet_id', 'planet_name', 'unsd_name')
#
#
# class RegionSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = Region
# 		fields = ('region_id', 'region_name', 'planet_id')
#
#
# class SubRegionSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = SubRegion
# 		fields = ('sub_region_id', 'sub_region_name', 'region_id')
#
#
# class IntermediateRegionSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = IntermediateRegion
# 		fields = ('intermediate_region_id', 'intermediate_region_name', 'sub_region_id')
#
#
# class LocationSerializer(serializers.ModelSerializer):
# 	planet = PlanetSerializer(many=False, read_only=True)
# 	region = RegionSerializer(many=False, read_only=True)
# 	sub_region = SubRegionSerializer(many=False, read_only=True)
# 	intermediate_region = IntermediateRegionSerializer(many=False, read_only=True)
#
# 	class Meta:
# 		model = Location
# 		fields = ('location_id', 'planet', 'region', 'sub_region', 'intermediate_region')
#
#
# class DevStatusSerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = DevStatus
# 		fields = ('dev_status_id', 'dev_status_name')
#
#
# class CountryAreaSerializer(serializers.ModelSerializer):
# 	dev_status = DevStatusSerializer(many=False, read_only=True)
# 	location = LocationSerializer(many=False, read_only=True)
#
# 	class Meta:
# 		model = CountryArea
# 		fields = (
# 			'country_area_id',
# 			'country_area_name',
# 			'm49_code',
# 			'iso_alpha3_code',
# 			'dev_status',
# 			'location')
#
#
# class HeritageSiteCategorySerializer(serializers.ModelSerializer):
#
# 	class Meta:
# 		model = HeritageSiteCategory
# 		fields = ('category_id', 'category_name')
#
#
# class HeritageSiteJurisdictionSerializer(serializers.ModelSerializer):
# 	heritage_site_id = serializers.ReadOnlyField(source='heritage_site.heritage_site_id')
# 	country_area_id = serializers.ReadOnlyField(source='country_area.country_area_id')
#
# 	class Meta:
# 		model = HeritageSiteJurisdiction
# 		fields = ('heritage_site_id', 'country_area_id')
#
#
# class HeritageSiteSerializer(serializers.ModelSerializer):
# 	site_name = serializers.CharField(
# 		allow_blank=False,
# 		max_length=255
# 	)
# 	description = serializers.CharField(
# 		allow_blank=False
# 	)
# 	justification = serializers.CharField(
# 		allow_blank=True
# 	)
# 	date_inscribed = serializers.IntegerField(
# 		allow_null=True
# 	)
# 	longitude = serializers.DecimalField(
# 		allow_null=True,
# 		max_digits=11,
# 		decimal_places=8)
# 	latitude = serializers.DecimalField(
# 		allow_null=True,
# 		max_digits=10,
# 		decimal_places=8
# 	)
# 	area_hectares = serializers.FloatField(
# 		allow_null=True
# 	)
# 	transboundary = serializers.IntegerField(
# 		allow_null=False
# 	)
# 	heritage_site_category = HeritageSiteCategorySerializer(
# 		many=False,
# 		read_only=True
# 	)
# 	heritage_site_category_id = serializers.PrimaryKeyRelatedField(
# 		allow_null=False,
# 		many=False,
# 		write_only=True,
# 		queryset=HeritageSiteCategory.objects.all(),
# 		source='heritage_site_category'
# 	)
# 	heritage_site_jurisdiction = HeritageSiteJurisdictionSerializer(
# 		source='heritage_site_jurisdiction_set', # Note use of _set
# 		many=True,
# 		read_only=True
# 	)
# 	jurisdiction_ids = serializers.PrimaryKeyRelatedField(
# 		many=True,
# 		write_only=True,
# 		queryset=CountryArea.objects.all(),
# 		source='heritage_site_jurisdiction'
# 	)
#
# 	class Meta:
# 		model = HeritageSite
# 		fields = (
# 			'heritage_site_id',
# 			'site_name',
# 			'description',
# 			'justification',
# 			'date_inscribed',
# 			'longitude',
# 			'latitude',
# 			'area_hectares',
# 			'transboundary',
# 			'heritage_site_category',
# 			'heritage_site_category_id',
# 			'heritage_site_jurisdiction',
# 			'jurisdiction_ids'
# 		)
#
# 	def create(self, validated_data):
# 		"""
# 		This method persists a new HeritageSite instance as well as adds all related
# 		countries/areas to the heritage_site_jurisdiction table.  It does so by first
# 		removing (validated_data.pop('heritage_site_jurisdiction')) from the validated
# 		data before the new HeritageSite instance is saved to the database. It then loops
# 		over the heritage_site_jurisdiction array in order to extract each country_area_id
# 		element and add entries to junction/associative heritage_site_jurisdiction table.
# 		:param validated_data:
# 		:return: site
# 		"""
#
# 		# print(validated_data)
#
# 		countries = validated_data.pop('heritage_site_jurisdiction')
# 		site = HeritageSite.objects.create(**validated_data)
#
# 		if countries is not None:
# 			for country in countries:
# 				HeritageSiteJurisdiction.objects.create(
# 					heritage_site_id=site.heritage_site_id,
# 					country_area_id=country.country_area_id
# 				)
# 		return site
#
# 	def update(self, instance, validated_data):
# 		# site_id = validated_data.pop('heritage_site_id')
# 		site_id = instance.heritage_site_id
# 		new_countries = validated_data.pop('heritage_site_jurisdiction')
#
# 		instance.site_name = validated_data.get(
# 			'site_name',
# 			instance.site_name
# 		)
# 		instance.description = validated_data.get(
# 			'description',
# 			instance.description
# 		)
# 		instance.justification = validated_data.get(
# 			'justification',
# 			instance.justification
# 		)
# 		instance.date_inscribed = validated_data.get(
# 			'date_inscribed',
# 			instance.date_inscribed
# 		)
# 		instance.longitude = validated_data.get(
# 			'longitude',
# 			instance.longitude
# 		)
# 		instance.latitude = validated_data.get(
# 			'latitude',
# 			instance.latitude
# 		)
# 		instance.area_hectares = validated_data.get(
# 			'area_hectares',
# 			instance.area_hectares
# 		)
# 		instance.heritage_site_category_id = validated_data.get(
# 			'heritage_site_category_id',
# 			instance.heritage_site_category_id
# 		)
# 		instance.transboundary = validated_data.get(
# 			'transboundary',
# 			instance.transboundary
# 		)
# 		instance.save()
#
# 		# If any existing country/areas are not in updated list, delete them
# 		new_ids = []
# 		old_ids = HeritageSiteJurisdiction.objects \
# 			.values_list('country_area_id', flat=True) \
# 			.filter(heritage_site_id__exact=site_id)
#
# 		# TODO Insert may not be required (Just return instance)
#
# 		# Insert new unmatched country entries
# 		for country in new_countries:
# 			new_id = country.country_area_id
# 			new_ids.append(new_id)
# 			if new_id in old_ids:
# 				continue
# 			else:
# 				HeritageSiteJurisdiction.objects \
# 					.create(heritage_site_id=site_id, country_area_id=new_id)
#
# 		# Delete old unmatched country entries
# 		for old_id in old_ids:
# 			if old_id in new_ids:
# 				continue
# 			else:
# 				HeritageSiteJurisdiction.objects \
# 					.filter(heritage_site_id=site_id, country_area_id=old_id) \
# 					.delete()
#
# 		return instance
