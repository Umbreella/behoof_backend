import graphene
from django.test import TestCase
from graphene import NonNull, Schema, relay
from graphene.test import Client

from ....models.Category import Category
from ....schema.types.CategoryType import CategoryType


class CategoryTypeTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CategoryType
        cls.model = Category

        Category.objects.bulk_create([
            Category(**{
                'id': 1,
                'title': 'title',
            }),
        ])

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
            'id', 'title',
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
                'id', 'title',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQuery_Should_ReturnDataWithoutErrors(self):
        response = self.gql_client.execute(
            """
            query {
                test (id: "Q2F0ZWdvcnlUeXBlOjE=") {
                    id
                    title
                }
            }
            """,
        )

        expected_data = {
            'data': {
                'test': {
                    'id': 'Q2F0ZWdvcnlUeXBlOjE=',
                    'title': 'title',
                },
            },
        }
        real_data = response

        self.assertEqual(expected_data, real_data)
