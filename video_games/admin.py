from django.contrib import admin

# Register your models here.
from django.contrib import admin

import video_games.models as models

# Developer Lookup Admin
@admin.register(models.Developer)
class DeveloperAdmin(admin.ModelAdmin):
    fields = ['developer_name']
    list_display = ['developer_name']
    ordering = ['developer_name']
    #NOTE CHECK
    #THIS IS THE M2M related CHECK may need to edit


# Region Lookup Admin
@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    fields = ['region_name']
    list_display = ['region_name']
    ordering = ['region_name']


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    fields = [
        'game_name',
        'platform',
        'year_released',
        'genre',
        'publisher',
        'critic_score',
        'critic_count',
        'user_score',
        'user_count',
        'rating'
    ]

    list_display  = [
        'game_name',
        'platform',
        'year_released',
        'genre',
        'publisher',
        'critic_score',
        'critic_count',
        'user_score',
        'user_count',
        'rating',
        'region_display',
        'developer_display'
    ]

    list_filter = [
        'platform',
        'genre'
    ]


# Genre Lookup Admin
@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    fields = ['genre_name']
    list_display = ['genre_name']
    ordering = ['genre_name']

# Platform Lookup Admin
@admin.register(models.Platform)
class PlatformAdmin(admin.ModelAdmin):
    fields = ['platform_name']
    list_display = ['platform_name']
    ordering = ['platform_name']

# Publisher Lookup Admin
@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    fields = ['publisher_name']
    list_display = ['publisher_name']
    ordering = ['publisher_name']

# Rating Lookup Admin
@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    fields = ['rating_name']
    list_display = ['rating_name']
    ordering = ['rating_name']




















#
#
#
#
#
#
#
#
#
#
#
#
#
# #HEREITAGE Sites
# #******************************************************
# #***********************************************
# @admin.register(models.CountryArea)
# class CountryAreaAdmin(admin.ModelAdmin):
# 	fields = [
# 		'country_area_name',
# 		(
# 			'region',
# 			'sub_region',
# 			'intermediate_region'
# 		),
# 		'iso_alpha3_code',
# 		'm49_code',
# 		'dev_status'
# 	]
#
# 	list_display = [
# 		'country_area_name',
# 		'region',
# 		'sub_region',
# 		'intermediate_region',
# 		'iso_alpha3_code',
# 		'm49_code',
# 		'dev_status'
# 	]
#
# 	list_filter = ['region', 'sub_region', 'intermediate_region', 'dev_status']
#
# # admin.site.register(models.CountryArea)
#
#
# @admin.register(models.DevStatus)
# class DevStatusAdmin(admin.ModelAdmin):
# 	fields = ['dev_status_name']
# 	list_display = ['dev_status_name']
# 	ordering = ['dev_status_name']
#
# # admin.site.register(models.DevStatus)
#
#
# @admin.register(models.HeritageSite)
# class HeritageSiteAdmin(admin.ModelAdmin):
# 	fieldsets = (
# 		(None, {
# 			'fields': (
# 				'site_name',
# 				'heritage_site_category',
# 				'description',
# 				'justification',
# 				'date_inscribed'
# 			)
# 		}),
# 		('Location and Area', {
# 			'fields': [
# 				(
# 					'longitude',
# 					'latitude'
# 				),
# 				'area_hectares',
# 				'transboundary'
# 			]
# 		})
# 	)
#
#
# 	list_display = (
# 		'site_name',
# 		'date_inscribed',
# 		'area_hectares',
# 		'heritage_site_category',
# 		'country_area_display'
# 	)
#
# 	list_filter = (
# 		'heritage_site_category',
# 		'date_inscribed'
# 	)
#
# # admin.site.register(models.HeritageSite)
#
#
# @admin.register(models.HeritageSiteCategory)
# class HeritageSiteCategoryAdmin(admin.ModelAdmin):
# 	fields = ['category_name']
# 	list_display = ['category_name']
# 	ordering = ['category_name']
#
# # admin.site.register(models.HeritageSiteCategory)
#
#
# @admin.register(models.IntermediateRegion)
# class IntermediateRegionAdmin(admin.ModelAdmin):
# 	fields = ['intermediate_region_name', 'sub_region']
# 	list_display = ['intermediate_region_name', 'sub_region']
# 	ordering = ['intermediate_region_name']
#
# # admin.site.register(models.IntermediateRegion)
#
#
# @admin.register(models.Region)
# class RegionAdmin(admin.ModelAdmin):
# 	fields = ['region_name']
# 	list_display = ['region_name']
# 	ordering = ['region_name']
#
# # admin.site.register(models.Region)
#
#
# @admin.register(models.SubRegion)
# class SubRegionAdmin(admin.ModelAdmin):
# 	fields = ['sub_region_name', 'region']
# 	list_display = ['sub_region_name', 'region']
# 	ordering = ['sub_region_name']
#
# # admin.site.register(models.SubRegion)
