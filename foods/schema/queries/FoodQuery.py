import graphene
from graphene_django.filter import DjangoFilterConnectionField

from behoof.graphql.nodes.IsPublichedNode import IsPublishedNode
from ...models.Food import Food
from ..filters.FoodFilter import FoodFilter
from ..types.FoodType import FoodType


class FoodQuery(graphene.ObjectType):
    food = IsPublishedNode.Field(FoodType)

    all_foods = DjangoFilterConnectionField(**{
        'type_': FoodType,
        'filterset_class': FoodFilter,
    })

    def resolve_all_foods(root, info, **kwargs):
        return Food.objects.filter(**{
            'is_published': True,
            'category__is_published': True,
        }).order_by('id')
