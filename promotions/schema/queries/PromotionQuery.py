import graphene
from graphene_django import DjangoConnectionField

from ...models.Promotion import Promotion
from ..types.PromotionType import PromotionType


class PromotionQuery(graphene.ObjectType):
    all_promotions = DjangoConnectionField(**{
        'type_': PromotionType,
    })

    def resolve_all_promotions(root, info, **kwargs):
        return Promotion.objects.all().order_by('id')
