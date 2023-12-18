import graphene
from django.test import TestCase
from django.utils import timezone
from graphene import Context, NonNull, Schema, relay, String
from graphene.test import Client

from behoof.graphql.nodes.IsPublichedNode import IsPublishedNode
from ....models.Promotion import Promotion
from ....schema.types.PromotionType import PromotionType


class PromotionTypeTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = PromotionType
        cls.model = Promotion

        cls.time_now = timezone.now()

        Promotion.objects.bulk_create([
            Promotion(**{
                'id': 1,
                'preview': 'preview',
                'title': 'title',
                'description': 'description' * 100,
                'is_published': True,
            }),
        ])

        context = Context()
        context.build_absolute_uri = lambda x: 'build_absolute_uri'
        cls.context = context

    def setUp(self):
        class TestQuery(graphene.ObjectType):
            test = IsPublishedNode.Field(self.tested_class)

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
            IsPublishedNode,
        ]
        real_interfaces = list(self.tested_class._meta.interfaces)

        self.assertEqual(expected_interfaces, real_interfaces)

    def test_Should_IncludeRequiredFieldsFromModel(self):
        expected_fields = [
            'id', 'preview', 'title', 'description', 'start_time', 'end_time',
            'preview_description',
        ]
        real_fields = list(self.tested_class._meta.fields)

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'preview_description': String,
        }
        real_fields = {
            key: value.type
            for key, value in self.tested_class._meta.fields.items()
        }

        all_fields_is_nonnull = all([
            real_fields.pop(field).__class__ == NonNull for field in [
                'id', 'preview', 'title', 'description', 'start_time',
                'end_time',
            ]
        ])

        self.assertEqual(expected_fields, real_fields)
        self.assertTrue(all_fields_is_nonnull)

    def test_When_SendQuery_Should_ReturnGEOJsonData(self):
        response = self.gql_client.execute(
            """
            query {
                test (id: "UHJvbW90aW9uVHlwZTox") {
                    id
                    preview
                    title
                    description
                    previewDescription
                }
            }
            """,
            context=self.context,
        )

        expected_data = {
            'data': {
                'test': {
                    'id': 'UHJvbW90aW9uVHlwZTox',
                    'preview': 'build_absolute_uri',
                    'title': 'title',
                    'description': 'description' * 100,
                    'previewDescription': ('description' * 100)[:254] + '…',
                },
            },
        }
        real_data = response

        self.maxDiff = None

        self.assertEqual(expected_data, real_data)
