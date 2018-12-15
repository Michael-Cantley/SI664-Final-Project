# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Reference for Developer
class Developer(models.Model):
    developer_id = models.AutoField(primary_key=True)
    developer_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'developer'

    def __str__(self):
        return self.developer_name

# Reference for Region
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.region_name

# Added str function
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255, blank=True, null=True)
    platform = models.ForeignKey('Platform', models.DO_NOTHING, blank=True, null=True)
    year_released = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey('Genre', models.DO_NOTHING, blank=True, null=True)
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING, blank=True, null=True)
    critic_score = models.IntegerField(blank=True, null=True)
    critic_count = models.IntegerField(blank=True, null=True)
    user_score = models.IntegerField(blank=True, null=True)
    user_count = models.IntegerField(blank=True, null=True)
    rating = models.ForeignKey('Rating', models.DO_NOTHING, blank=True, null=True)

    # Intermediate model (region -> sales <- game)
    region = models.ManyToManyField(Region, through='Sale')
    # Intermediate model (developer > game_developer <- game)
    developer = models.ManyToManyField(Developer, through='GameDeveloper')

    class Meta:
        managed = False
        db_table = 'game'

    def __str__(self):
        return self.game_name

    def region_display(self):
        '''Create a region string. This is required to display in Admin view.'''
        return ', '.join(
            region.region_name for region in self.region.all()[:25])

    region_display.short_description = 'Region'

    def developer_display(self):
        '''Create a string for developer. Required for display in Admin View.'''
        return ', '.join(
            developer.developer_name for developer in self.developer.all()[:25])

    developer_display.short_description = 'Developer'

# Linking table b/w Game and Developer to handle the M2M relationship
class GameDeveloper(models.Model):
    game_developer_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, models.DO_NOTHING)
    developer = models.ForeignKey(Developer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'game_developer'

# Reference for Genre
class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'genre'

    def __str__(self):
        return self.genre_name


class Platform(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'platform'

    def __str__(self):
        return self.platform_name


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    publisher_name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'publisher'

    def __str__(self):
        return self.publisher_name


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    rating_name = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'rating'

    def __str__(self):
        return self.rating_name


#"Linking table" b/w Region and Game to handle the M2M relationship
class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, models.DO_NOTHING)
    region = models.ForeignKey(Region, models.DO_NOTHING)
    total_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sale'


class TempGame(models.Model):
    game_id = models.AutoField(primary_key=True)
    game_name = models.CharField(max_length=255)
    platform_name = models.CharField(max_length=50, blank=True, null=True)
    year_released = models.CharField(max_length=4, blank=True, null=True)
    genre_name = models.CharField(max_length=25, blank=True, null=True)
    publisher_name = models.CharField(max_length=100, blank=True, null=True)
    north_america_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    europe_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    japan_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    other_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    global_sales = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    critic_score = models.CharField(max_length=3, blank=True, null=True)
    critic_count = models.CharField(max_length=10, blank=True, null=True)
    user_score = models.CharField(max_length=3, blank=True, null=True)
    user_count = models.CharField(max_length=10, blank=True, null=True)
    developer_name = models.CharField(max_length=100, blank=True, null=True)
    rating_name = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_game'
