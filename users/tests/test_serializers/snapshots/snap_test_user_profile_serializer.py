# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots['UserProfileSerializerTestCase::test_Should_SpecificFormatForEachField 1'] = '''UserProfileSerializer():
    first_name = CharField(max_length=150, required=True)
    last_name = CharField(max_length=150, required=True)
    email = EmailField(max_length=254, required=True)
    phone_number = PhoneNumberField()
    password = CharField(write_only=True)'''
