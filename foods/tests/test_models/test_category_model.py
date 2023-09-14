from django.core.exceptions import ValidationError
from django.db.models import (
    BigAutoField, BooleanField, CharField, ManyToOneRel,
)
from django.test import TestCase

from ...models.Category import Category


class CategoryTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Category

        cls.data = {
            'title': 'title',
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'foods', 'id', 'title', 'is_published',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'foods': ManyToOneRel,
            'id': BigAutoField,
            'title': CharField,
            'is_published': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'foods': '',
            'id': '',
            'title': 'Category title.',
            'is_published': 'Displayed to the user.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateInstanceWithOutData_Should_ErrorBlankField(self):
        instance = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            instance.save()

        expected_raise = {
            'title': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThanMaxLenght_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'title': 'q' * 256,
        })

        instance = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            instance.save()

        expected_raise = {
            'title': [
                'Ensure this value has at most 255 characters (it has 256).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveInstanceAndReturnTitleAsStr(self):
        data = self.data

        instance = self.tested_class(**data)
        instance.save()

        expected_str = f'{instance.title}'
        real_str = str(instance)

        expected_is_published = False
        real_is_published = instance.is_published

        self.assertEqual(expected_str, real_str)
        self.assertEqual(expected_is_published, real_is_published)
