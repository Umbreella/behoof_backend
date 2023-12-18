import graphene
from django.template.defaultfilters import truncatechars
from graphene_django import DjangoObjectType

from behoof.graphql.nodes.IsPublichedNode import IsPublishedNode
from ...models.Promotion import Promotion


class PromotionType(DjangoObjectType):
    preview_description = graphene.String()

    class Meta:
        model = Promotion
        fields = (
            'id', 'preview', 'title', 'description', 'start_time', 'end_time',
        )
        interfaces = (IsPublishedNode,)

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)

    def resolve_preview_description(self, info):
        return truncatechars(self.description, 255)
