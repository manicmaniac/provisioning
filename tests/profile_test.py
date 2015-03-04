#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os.path
import sys
import datetime
import uuid
import platform
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from provisioning.profile import ProvisioningProfile, stored_provisioning_profiles
from provisioning.entitlements import Entitlements


class ProvisioningProfileTests(unittest.TestCase):
    def setUp(self):
        path = os.path.join(os.path.dirname(__file__), 'test.mobileprovision')
        with open(path) as f:
            self.data = f.read()
        self.profile = ProvisioningProfile(self.data)
        assert self.profile

    def test_is_expired(self):
        date = datetime.datetime(2015, 1, 1)
        self.assertTrue(self.profile.is_expired(date))

    def test_data(self):
        self.assertEqual(self.profile.data, self.data)

    def test_application_identifier_prefix(self):
        self.assertListEqual(self.profile.application_identifier_prefix, ['NVY25AP72H'])

    def test_creation_date(self):
        date = datetime.datetime(2011, 1, 5, 18, 31, 50)
        self.assertEqual(self.profile.creation_date, date)

    def test_developer_certificates(self):
        self.assertEqual(len(self.profile.developer_certificates), 13)

    def test_entitlements(self):
        self.assertIsInstance(self.profile.entitlements, Entitlements)

    def test_expiration_date(self):
        date = datetime.datetime(2011, 4, 5, 18, 31, 50)
        self.assertEqual(self.profile.expiration_date, date)

    def test_name(self):
        self.assertEqual(self.profile.name, 'Team Provisioning Profile: *')

    def test_provisioned_devices(self):
        self.assertEqual(len(self.profile.provisioned_devices), 65)

    def test_time_to_live(self):
        self.assertEqual(self.profile.time_to_live, 90)

    def test_uuid(self):
        self.assertIsInstance(self.profile.uuid, uuid.UUID)

    def test_version(self):
        self.assertEqual(self.profile.version, '1')

    def test_stored_provisioning_profiles(self):
        if platform.system() == 'Darwin':
            profiles = stored_provisioning_profiles()
            self.assertIsInstance(profiles, list)
        else:
            with self.assertRaises(OSError):
                stored_provisioning_profiles()


if __name__ == '__main__':
    unittest.main()

