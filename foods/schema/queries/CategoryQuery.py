import graphene
from graphene_django import DjangoConnectionField

from ...models.Category import Category
from ..types.CategoryType import CategoryType


class CategoryQuery(graphene.ObjectType):
    all_categories = DjangoConnectionField(**{
        'type_': CategoryType,
    })

    def resolve_all_categories(root, info, **kwargs):
        return Category.objects.filter(**{
            'is_published': True,
        }).order_by('id')
