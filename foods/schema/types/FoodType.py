import graphene
from graphene_django import DjangoObjectType

from ...models.Food import Food
from ..nodes.FoodNode import FoodNode


class FoodType(DjangoObjectType):
    price = graphene.Float()
    weight = graphene.Int()
    proteins = graphene.Float()
    fats = graphene.Float()
    carbohydrates = graphene.Float()
    kilocalories = graphene.Float()

    class Meta:
        model = Food
        fields = (
            'id', 'preview', 'title', 'composition', 'description', 'price',
            'weight', 'proteins', 'fats', 'carbohydrates', 'kilocalories',
        )
        interfaces = (FoodNode,)

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)
