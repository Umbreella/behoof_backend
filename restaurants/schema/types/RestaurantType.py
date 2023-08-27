from graphene import relay
from graphene_django import DjangoObjectType
from graphene_gis.converter import gis_converter  # noqa

from ...models.Restaurant import Restaurant


class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = (
            'id', 'address', 'geo_position', 'coverage_area',
        )
        interfaces = (relay.Node,)
