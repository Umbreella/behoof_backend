import graphene
from django.contrib.gis.geos import Point, Polygon
from django.test import TestCase
from graphene import NonNull, Schema, relay
from graphene.test import Client

from ....models.Restaurant import Restaurant
from ....schema.types.RestaurantType import RestaurantType


class RestaurantTypeTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RestaurantType
        cls.model = Restaurant

        Restaurant.objects.create(**{
            'id': 1,
            'address': 'address',
            'geo_position': Point(0, 0),
            'coverage_area': Polygon(
                (
                    (0, 0), (0, 1), (1, 1), (1, 0), (0, 0),
                ),
            ),
        })

    def setUp(self):
        class TestQuery(graphene.ObjectType):
            test = relay.Node.Field(self.tested_class)

        self.gql_client = Client(**{
            'schema': Schema(**{
                'query': TestQuery,
            }),
        })

    def test_Should_IncludeDefiniteDjangoModel(self):
        expected_model = self.model
        real_model = self.tested_class._meta.model

        self.assertEqual(expected_model, real_model)

    def test_Should_IncludeDefiniteInterfaces(self):
        expected_interfaces = [
            relay.Node,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeRequiredFieldsFromModel(self):
        expected_fields = [
            'id', 'address', 'geo_position', 'coverage_area',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {}
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'address', 'geo_position', 'coverage_area',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQuery_Should_ReturnGEOJsonData(self):
        response = self.gql_client.execute(
            """
            query {
                test (id: "UmVzdGF1cmFudFR5cGU6MQ==") {
                    id
                    address
                    geoPosition
                    coverageArea
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'test': {
                    'id': 'UmVzdGF1cmFudFR5cGU6MQ==',
                    'address': 'address',
                    'geoPosition': {
                        'type': 'Point',
                        'coordinates': [
                            0.0, 0.0,
                        ],
                    },
                    'coverageArea': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [
                                    0.0, 0.0,
                                ],
                                [
                                    0.0, 1.0,
                                ],
                                [
                                    1.0, 1.0,
                                ],
                                [
                                    1.0, 0.0,
                                ],
                                [
                                    0.0, 0.0,
                                ],
                            ],
                        ],
                    },
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
