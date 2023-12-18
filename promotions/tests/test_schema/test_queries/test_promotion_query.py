from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from ....models.Promotion import Promotion
from ....schema.queries.PromotionQuery import PromotionQuery


class PromotionQueryTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PromotionQuery

        Promotion.objects.bulk_create([
            Promotion(**{
                'id': 3,
                'preview': 'preview',
                'title': 'title',
                'description': 'description',
                'is_published': True,
            }),
            Promotion(**{
                'id': 2,
                'preview': 'preview',
                'title': 'title',
                'description': 'description',
                'is_published': True,
            }),
            Promotion(**{
                'id': 1,
                'preview': 'preview',
                'title': 'title',
                'description': 'description',
            }),
        ])

    def setUp(self) -> None:
        self.gql_client = Client(**{
            'schema': Schema(**{
                'query': self.tested_class,
            }),
        })

    def test_When_SendQueryWithAllRestaurants_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                allPromotions {
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
                'allPromotions': {
                    'edges': [
                        {
                            'node': {
                                'id': 'UHJvbW90aW9uVHlwZToy',
                            },
                        },
                        {
                            'node': {
                                'id': 'UHJvbW90aW9uVHlwZToz',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
