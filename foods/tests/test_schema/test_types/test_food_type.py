import graphene
from django.test import TestCase
from graphene import Context, NonNull, Schema
from graphene.test import Client

from ....models.Category import Category
from ....models.Food import Food
from ....schema.nodes.FoodNode import FoodNode
from ....schema.types.FoodType import FoodType


class FoodTypeTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = FoodType
        cls.model = Food

        Category.objects.bulk_create([
            Category(**{
                'id': 1,
                'title': 'title_1',
                'is_published': True,
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
                'kilocalories': 10.0,
                'is_published': True,
            }),
        ])

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        cls.context = context

    def setUp(self):
        class TestQuery(graphene.ObjectType):
            test = FoodNode.Field(self.tested_class)

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
            FoodNode,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeRequiredFieldsFromModel(self):
        expected_fields = [
            'id', 'preview', 'title', 'composition', 'description', 'price',
            'weight', 'proteins', 'fats', 'carbohydrates', 'kilocalories',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'price': graphene.Float,
            'weight': graphene.Int,
            'proteins': graphene.Float,
            'fats': graphene.Float,
            'carbohydrates': graphene.Float,
            'kilocalories': graphene.Float,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'preview', 'title', 'composition', 'description',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQuery_Should_ReturnGEOJsonData(self):
        response = self.gql_client.execute(
            """
            query {
                test (id: "Rm9vZFR5cGU6MQ==") {
                    id
                    preview
                    title
                    composition
                    description
                    price
                    weight
                    proteins
                    fats
                    carbohydrates
                    kilocalories
                }
            }
            """,
            context=self.context,
        )

        expected_data = {
            'data': {
                'test': {
                    'id': 'Rm9vZFR5cGU6MQ==',
                    'title': 'title',
                    'preview': 'build_absolute_uri',
                    'composition': 'composition',
                    'description': 'description',
                    'price': 100.0,
                    'weight': 100,
                    'proteins': 10.0,
                    'fats': 10.0,
                    'carbohydrates': 10.0,
                    'kilocalories': 10.0,
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
