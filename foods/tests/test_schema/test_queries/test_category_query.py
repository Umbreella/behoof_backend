from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from ....models.Category import Category
from ....schema.queries.CategoryQuery import CategoryQuery


class CategoryQueryTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryQuery

        Category.objects.bulk_create([
            Category(**{
                'id': 3,
                'title': 'title',
                'is_published': True,
            }),
            Category(**{
                'id': 2,
                'title': 'title',
            }),
            Category(**{
                'id': 1,
                'title': 'title',
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
                allCategories {
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
                'allCategories': {
                    'edges': [
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjE=',
                            },
                        },
                        {
                            'node': {
                                'id': 'Q2F0ZWdvcnlUeXBlOjM=',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
