from graphene import relay
from graphene_django import DjangoObjectType

from ...models.Category import Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = (
            'id', 'title',
        )
        interfaces = (relay.Node,)
