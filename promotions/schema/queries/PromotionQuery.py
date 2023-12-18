from graphene import ObjectType
from graphene_django import DjangoConnectionField

from behoof.graphql.nodes.IsPublichedNode import IsPublishedNode
from ...models.Promotion import Promotion
from ..types.PromotionType import PromotionType


class PromotionQuery(ObjectType):
    promotion = IsPublishedNode.Field(PromotionType)

    all_promotions = DjangoConnectionField(**{
        'type_': PromotionType,
    })

    def resolve_all_promotions(root, info, **kwargs):
        return Promotion.objects.filter(is_published=True).order_by('id')
