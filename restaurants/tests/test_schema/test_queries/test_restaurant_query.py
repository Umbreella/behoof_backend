from django.contrib.gis.geos import Point, Polygon
from django.test import TestCase
from graphene import Schema
from graphene.test import Client

from ....models.Restaurant import Restaurant
from ....schema.queries.RestaurantQuery import RestaurantQuery


class RestaurantQueryTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RestaurantQuery

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
                allRestaurants {
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
                'allRestaurants': {
                    'edges': [
                        {
                            'node': {
                                'id': 'UmVzdGF1cmFudFR5cGU6MQ==',
                            },
                        },
                        {
                            'node': {
                                'id': 'UmVzdGF1cmFudFR5cGU6Mg==',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)

    def test_When_SendQueryWithAllRes_Should_ReturnWithOutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                allRestaurants (position: "[0, 0]") {
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
                'allRestaurants': {
                    'edges': [
                        {
                            'node': {
                                'id': 'UmVzdGF1cmFudFR5cGU6MQ==',
                            },
                        },
                    ],
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
