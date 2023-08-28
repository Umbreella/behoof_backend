import graphene
from django.test import TestCase
from graphene import Schema, relay
from graphene.test import Client

from ....models.Category import Category
from ....models.Food import Food
from ....schema.nodes.FoodNode import FoodNode
from ....schema.types.FoodType import FoodType


class FoodNodeTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FoodNode

        Category.objects.bulk_create([
            Category(**{
                'id': 1,
                'title': 'title_1',
            }),
        ])

        Food.objects.bulk_create([
            Food(**{
                'id': 1,
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
            }),
        ])

    def setUp(self):
        class TestQuery(graphene.ObjectType):
            test = self.tested_class.Field(FoodType)

        self.gql_client = Client(**{
            'schema': Schema(**{
                'query': TestQuery,
            }),
        })

    def test_Should_InheritRelayNode(self):
        expected_super_classes = (
            relay.Node,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_When_NodeNotIsPublished_Should_ReturnNone(self):
        response = self.gql_client.execute(
            """
            query {
                first_test: test (id: "Rm9vZFR5cGU6MQ==") {
                    id
                }
                second_test: test (id: "Rm9vZFR5cGU6Mg==") {
                    id
                }
                third_test: test (id: "Rm9vZFR5cGU6Mw==") {
                    id
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'first_test': {
                    'id': 'Rm9vZFR5cGU6MQ==',
                },
                'second_test': None,
                'third_test': None,
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
