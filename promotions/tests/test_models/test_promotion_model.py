from django.contrib.gis.db.models import BigAutoField, CharField
from django.core.exceptions import ValidationError
from django.db.models import DateTimeField, ImageField, TextField
from django.test import TestCase
from django.utils import timezone

from ...models.Promotion import Promotion


class PromotionTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Promotion

        cls.data = {
            'preview': 'preview',
            'title': 'title',
            'description': 'description',
        }

        cls.date_format = '%H:%M %d-%m-%Y'

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'preview', 'title', 'description', 'start_time', 'end_time',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'preview': ImageField,
            'title': CharField,
            'description': TextField,
            'start_time': DateTimeField,
            'end_time': DateTimeField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'preview': 'Promotion preview.',
            'title': 'Promotion title.',
            'description': 'Promotion description.',
            'start_time': 'Promotion start time.',
            'end_time': 'Promotion start time.',
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
            'preview': [
                'This field cannot be blank.',
            ],
            'title': [
                'This field cannot be blank.',
            ],
            'description': [
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

    def test_When_AllDataIsValid_Should_SaveInstanceAndReturnTitleAsStr(
            self,
    ):
        data = self.data

        instance = self.tested_class(**data)
        instance.save()

        expected_str = f'{instance.title}'
        real_str = str(instance)

        expected_start_time = timezone.now().strftime(self.date_format)
        real_start_time = instance.start_time.strftime(self.date_format)

        expected_end_time = timezone.now().strftime(self.date_format)
        real_end_time = instance.end_time.strftime(self.date_format)

        self.assertEqual(expected_str, real_str)
        self.assertEqual(expected_start_time, real_start_time)
        self.assertEqual(expected_end_time, real_end_time)
