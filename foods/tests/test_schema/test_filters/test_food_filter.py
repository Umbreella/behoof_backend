from django.test import TestCase
from django_filters import CharFilter
from graphql import GraphQLError

from ....models.Category import Category
from ....models.Food import Food
from ....schema.filters.FoodFilter import FoodFilter


class FoodFilterTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FoodFilter
        cls.queryset = Food.objects.all()

        Category.objects.bulk_create([
            Category(**{
                'id': 1,
                'title': 'title',
            }),
            Category(**{
                'id': 2,
                'title': 'title',
            }),
        ])

        Food.objects.bulk_create([
            Food(**{
                'id': 2,
                'category_id': 1,
                'preview': 'tmp_file',
                'title': 'title',
                'composition': 'composition',
                'description': 'description',
                'price': 100,
                'weight': 100,
                'proteins': 10.0,
                'fats': 10.0,
                'carbohydrates': 10.0,
                'kilocalories': 100,
                'is_published': True,
            }),
            Food(**{
                'id': 1,
                'category_id': 2,
                'preview': 'tmp_file',
                'title': 'title',
                'composition': 'composition',
                'description': 'description',
                'price': 100,
                'weight': 100,
                'proteins': 10.0,
                'fats': 10.0,
                'carbohydrates': 10.0,
                'kilocalories': 100,
                'is_published': True,
            }),
        ])

    def test_Should_IncludeDefiniteFilters(self):
        expected_filters = [
            'category',
        ]
        real_filters = list(self.tested_class.get_filters())

        self.assertEqual(expected_filters, real_filters)

    def test_Should_SpecificTypeForEachFilter(self):
        expected_filters = {
            'category': CharFilter,
        }
        real_filters = {
            key: value.__class__
            for key, value in self.tested_class.get_filters().items()
        }

        self.assertEqual(expected_filters, real_filters)

    def test_When_CategoryIsNotValid_Should_ReturnGraphQLError(self):
        data = {
            'category': 'Rm9vZFR5cGU6MQ==',
        }
        filter_ = self.tested_class(data=data, queryset=self.queryset)

        with self.assertRaises(GraphQLError) as _raise:
            filter_.qs

        expected_raise = 'category: not valid value.'
        real_raise = _raise.exception.message

        self.assertEqual(expected_raise, real_raise)

    def test_When_CategoryIsValid_Should_ReturnData(self):
        data = {
            'category': 'Q2F0ZWdvcnlUeXBlOjE=',
        }
        filter_ = self.tested_class(data=data, queryset=self.queryset)

        expected_raise = list(self.queryset.filter(category_id=1))
        real_raise = list(filter_.qs)

        self.assertEqual(expected_raise, real_raise)
