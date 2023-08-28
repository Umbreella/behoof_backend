from django_filters import CharFilter, FilterSet
from graphql import GraphQLError
from graphql_relay import from_global_id

from ..types.CategoryType import CategoryType


class FoodFilter(FilterSet):
    category = CharFilter(**{
        'method': '_category_filter',
    })

    def _category_filter(self, queryset, name, value):
        type_, category_id = from_global_id(value)

        if type_ != CategoryType.__name__:
            raise GraphQLError('category: not valid value.')

        queryset = queryset.filter(**{
            'category': category_id,
        })

        return queryset
