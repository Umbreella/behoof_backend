import json

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters import CharFilter, FilterSet
from graphql import GraphQLError


class RestaurantFilter(FilterSet):
    position = CharFilter(**{
        'method': '_position_filter',
    })

    def _position_filter(self, queryset, name, value):
        try:
            position = [float(item) for item in json.loads(value)]
            assert len(position) == 2
        except Exception:
            detail = 'Position can`t converted to [lat, lon]'
            raise GraphQLError(detail)

        user_location = Point(position[1], position[0], srid=4326)

        queryset = queryset.annotate(**{
            'distance': Distance('geo_position', user_location),
        }).order_by(
            'distance',
        )[:1]

        return queryset
