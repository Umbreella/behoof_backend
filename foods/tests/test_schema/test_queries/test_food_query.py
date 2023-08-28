from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from ....models.Category import Category
from ....models.Food import Food
from ....schema.queries.FoodQuery import FoodQuery


class FoodQueryTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FoodQuery

        Category.objects.bulk_create([
            Category(**{
                'id': 1,
                'title': 'title',
                'is_published': True,
            }),
            Category(**{
                'id': 2,
                'title': 'title',
            }),
            Category(**{
                'id': 3,
                'title': 'title',
                'is_published': True,
            }),
        ])

        Food.objects.bulk_create([
            Food(**{
                'id': 4,
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
                'kilocalories': 10.0,
                'is_published': True,
            }),
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
                'kilocalories': 10.0,
            }),
            Food(**{
                'id': 3,
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
                'kilocalories': 10.0,
                'is_published': True,
            }),
            Food(**{
                'id': 1,
                'category_id': 3,
                'preview': 'tmp_file',
                'title': 'title',
                'composition': 'composition',
                'description': 'description',
                'price': 100,
                'weight': 100,
                'proteins': 10.0,
                'fats': 10.0,
                'carbohydrates': 10.0,
                'kilocalories': 10.0,
                'is_published': True,
            }),
        ])

    def setUp(self) -> None:
        self.gql_client = Client(**{
            'schema': Schema(**{
                'query': self.tested_class,
            }),
        })

    def test_When_SendQueryWithAllCategories_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                food (id: "Rm9vZFR5cGU6MQ==") {
                    id
                }
                allFoods {
                    edges {
                        node {
                            id
                        }
                    }
                }
                filterAllFoods: allFoods (category: "Q2F0ZWdvcnlUeXBlOjE=") {
                    edges {
                        node {
                            id
                        }
                    }
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'food': {
                    'id': 'Rm9vZFR5cGU6MQ==',
                },
                'filterAllFoods': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Rm9vZFR5cGU6NA==',
                            },
                        },
                    ],
                },
                'allFoods': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Rm9vZFR5cGU6MQ==',
                            },
                        },
                        {
                            'node': {
                                'id': 'Rm9vZFR5cGU6NA==',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
