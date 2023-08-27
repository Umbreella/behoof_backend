from django.contrib.gis.geos import Point, Polygon
from django.test import TestCase
from django_filters import CharFilter
from graphql import GraphQLError

from ....models.Restaurant import Restaurant
from ....schema.filters.RestaurantFilter import RestaurantFilter


class RestaurantFilterTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RestaurantFilter
        cls.queryset = Restaurant.objects.all()

        Restaurant.objects.bulk_create([
            Restaurant(**{
                'id': 1,
                'address': 'address_1',
                'geo_position': Point(0, 0),
                'coverage_area': Polygon(
                    (
                        (0, 0), (0, 1), (1, 1), (1, 0), (0, 0),
                    ),
                ),
            }),
            Restaurant(**{
                'id': 2,
                'address': 'address_2',
                'geo_position': Point(1, 1),
                'coverage_area': Polygon(
                    (
                        (1, 1), (1, 2), (2, 2), (2, 1), (1, 1),
                    ),
                ),
            }),
        ])

    def test_Should_IncludeDefiniteFilters(self):
        expected_filters = [
            'position',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachFilter(self):
        expected_filters = {
            'position': CharFilter,
        }
        real_filters = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_filters, real_filters)

    def test_When_PositionIsString_Should_GraphQLError(self):
        filter_ = self.tested_class(**{
            'data': {
                'position': '1, 2, 3, ',
            },
            'queryset': self.queryset,
        })

        with self.assertRaises(GraphQLError) as _raise:
            filter_.qs

        expected_raise = 'Position can`t converted to [lat, lon]'
        real_raise = _raise.exception.message

        self.assertEqual(expected_raise, real_raise)

    def test_When_PositionIsLongList_Should_GraphQLError(self):
        filter_ = self.tested_class(**{
            'data': {
                'position': '[1, 2, 3,]',
            },
            'queryset': self.queryset,
        })

        with self.assertRaises(GraphQLError) as _raise:
            filter_.qs

        expected_raise = 'Position can`t converted to [lat, lon]'
        real_raise = _raise.exception.message

        self.assertEqual(expected_raise, real_raise)

    def test_When_PositionIsValid_Should_ReturnNearestRestaurant(self):
        filter_ = self.tested_class(**{
            'data': {
                'position': '[0, 0]',
            },
            'queryset': self.queryset,
        })

        expected_queryset = list(self.queryset.filter(id=1))
        real_queryset = list(filter_.qs)

        self.assertEqual(expected_queryset, real_queryset)
