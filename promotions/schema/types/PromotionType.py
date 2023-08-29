from graphene import relay
from graphene_django import DjangoObjectType

from ...models.Promotion import Promotion


class PromotionType(DjangoObjectType):
    class Meta:
        model = Promotion
        fields = (
            'id', 'preview', 'title', 'description', 'start_time', 'end_time',
        )
        interfaces = (relay.Node,)

    def resolve_preview(self, info):
        return info.context.build_absolute_uri(self.preview.url)
