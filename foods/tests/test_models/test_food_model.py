import decimal
import tempfile

from django.core.exceptions import ValidationError
from django.db.models import (
    BigAutoField, BooleanField, CharField, DecimalField, ForeignKey,
    ImageField, PositiveIntegerField, TextField,
)
from django.test import TestCase

from ...models.Category import Category
from ...models.Food import Food


class FoodTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Food

        category = Category(**{
            'title': 'title',
        })
        category.save(force_insert=False)

        cls.data = {
            'category': category,
            'preview': tempfile.NamedTemporaryFile(suffix='.jpg').name,
            'title': 'title',
            'composition': 'composition',
            'description': 'description',
            'price': 100,
            'weight': 100,
            'proteins': 10.0,
            'fats': 10.0,
            'carbohydrates': 10.0,
            'kilocalories': 10.0,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'category', 'preview', 'title', 'composition', 'description',
            'price', 'weight', 'proteins', 'fats', 'carbohydrates',
            'kilocalories', 'is_published',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'category': ForeignKey,
            'preview': ImageField,
            'title': CharField,
            'composition': TextField,
            'description': TextField,
            'price': DecimalField,
            'weight': PositiveIntegerField,
            'proteins': DecimalField,
            'fats': DecimalField,
            'carbohydrates': DecimalField,
            'kilocalories': DecimalField,
            'is_published': BooleanField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'category': 'Food category.',
            'preview': 'Food preview.',
            'title': 'Food title.',
            'composition': 'Composition of the food.',
            'description': 'Food description.',
            'price': 'Food price',
            'weight': 'Food weight in grams.',
            'proteins': 'Amount of proteins.',
            'fats': 'Amount of fats.',
            'carbohydrates': 'Amount of carbohydrates.',
            'kilocalories': 'Amount of kilocalories.',
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
            'carbohydrates': [
                'This field cannot be null.',
            ],
            'category': [
                'This field cannot be blank.',
            ],
            'composition': [
                'This field cannot be blank.',
            ],
            'description': [
                'This field cannot be blank.',
            ],
            'fats': [
                'This field cannot be null.',
            ],
            'kilocalories': [
                'This field cannot be null.',
            ],
            'preview': [
                'This field cannot be blank.',
            ],
            'price': [
                'This field cannot be null.',
            ],
            'proteins': [
                'This field cannot be null.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
            'weight': [
                'This field cannot be null.',
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

    def test_When_FloatMoreThanDecimalPlaces_Should_CreateInstance(self):
        data = self.data
        data.update({
            'price': decimal.Decimal(0.12345),
            'proteins': decimal.Decimal(0.12345),
            'fats': decimal.Decimal(0.12345),
            'carbohydrates': decimal.Decimal(0.12345),
            'kilocalories': decimal.Decimal(0.12345),
        })

        instance = self.tested_class(**data)
        instance.save()

        expected_price = 0.12
        real_price = float(instance.price)

        expected_proteins = 0.1
        real_proteins = float(instance.proteins)

        expected_fats = 0.1
        real_fats = float(instance.fats)

        expected_carbohydrates = 0.1
        real_carbohydrates = float(instance.carbohydrates)

        expected_kilocalories = 0.1
        real_kilocalories = float(instance.kilocalories)

        self.assertEqual(expected_price, real_price)
        self.assertEqual(expected_proteins, real_proteins)
        self.assertEqual(expected_fats, real_fats)
        self.assertEqual(expected_carbohydrates, real_carbohydrates)
        self.assertEqual(expected_kilocalories, real_kilocalories)

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
