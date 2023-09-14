from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from graphene_django.views import GraphQLView
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Behoof API',
        default_version='v1',
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path(**{
        'route': 'api/docs/',
        'view': schema_view.with_ui('swagger', cache_timeout=0),
        'name': 'schema-swagger-ui',
    }),
    path('api/admin/', admin.site.urls),

    path('api/users/', include('users.urls')),

    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/docs/', GraphQLView.as_view(graphiql=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
