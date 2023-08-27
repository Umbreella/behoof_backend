import graphene
from graphene_django.filter import DjangoFilterConnectionField

from ...models.Restaurant import Restaurant
from ..filters.RestaurantFilter import RestaurantFilter
from ..types.RestaurantType import RestaurantType


class RestaurantQuery(graphene.ObjectType):
    all_restaurants = DjangoFilterConnectionField(**{
        'type_': RestaurantType,
        'filterset_class': RestaurantFilter,
    })

    def resolve_all_restaurants(root, info, **kwargs):
        return Restaurant.objects.all().order_by('id')
