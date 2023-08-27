from django.contrib.gis.db.models import (BigAutoField, CharField, PointField,
                                          PolygonField)
from django.contrib.gis.geos import Point, Polygon
from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models.Restaurant import Restaurant


class RestaurantTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = Restaurant

        cls.data = {
            'address': 'address',
            'geo_position': Point(0, 0),
            'coverage_area': Polygon(
                (
                    (0, 0), (0, 1), (1, 1), (1, 0), (0, 0),
                ),
            ),
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'id', 'address', 'geo_position', 'coverage_area',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'id': BigAutoField,
            'address': CharField,
            'geo_position': PointField,
            'coverage_area': PolygonField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'id': '',
            'address': 'Human readable address',
            'geo_position': '',
            'coverage_area': '',
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
            'address': [
                'This field cannot be blank.',
            ],
            'geo_position': [
                'This field cannot be null.',
            ],
            'coverage_area': [
                'This field cannot be null.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThanMaxLenght_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'address': 'q' * 256,
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'address': [
                'Ensure this value has at most 255 characters (it has 256).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveInstanceAndReturnAddressAsStr(
            self,
    ):
        data = self.data

        instance = self.tested_class(**data)
        instance.save()

        expected_str = f'{instance.address}'
        real_str = str(instance)

        self.assertEqual(expected_str, real_str)
