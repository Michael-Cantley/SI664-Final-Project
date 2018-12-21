from django.urls import include, path
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view
from api.views import GameViewSet, DeveloperViewSet
from rest_framework import routers

API_TITLE = 'video_games API'
API_DESC = 'A web API for creating, modifying and deleting Video Games and/or Game Developers.'

docs_view = include_docs_urls(
	title=API_TITLE,
	description=API_DESC
)

# Swagger view
schema_view = get_swagger_view(title=API_TITLE)

# Default view
'''
schema_view = get_schema_view(
	title=API_TITLE,
	# renderer_classes=[OpenAPIRenderer]
)
'''

router = routers.SimpleRouter()
router.register(r'games', GameViewSet, base_name='games')
# router2 = SimpleRouter()
router.register('developers', DeveloperViewSet, base_name='developers')
# urlpatterns = router.urls

# The API URLs are now determined automatically by the router.
urlpatterns = [
	path('', include(router.urls)),
	path('docs/', docs_view),
	path('swagger-docs/', schema_view)
	# path('schema/', schema_view)
]

#urlpatterns += router.urls

'''
urlpatterns = [
	path('schema/', schema_view),
	path('sites/', views.SiteListAPIView.as_view(), name='site_api'),
	path('sites/<int:pk>/', views.SiteDetailAPIView.as_view(), name='site_detail_api'),
]
'''
