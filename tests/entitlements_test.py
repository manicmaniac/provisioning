#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import os.path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from provisioning.entitlements import Entitlements 


class EntitlementsTests(unittest.TestCase):
    def setUp(self):
        self.entitlements = Entitlements.from_dict({
            'application-identifier': 'SPAMHAMEGG.*',
            'get-task-allow': True,
            'keychain-access-groups': ['SPAMHAMEGG.*'],
            })
        assert self.entitlements

    def test_application_identifier(self):
        self.assertEqual(self.entitlements.application_identifier, 'SPAMHAMEGG.*')

    def test_get_task_allow(self):
        self.assertTrue(self.entitlements.get_task_allow)

    def test_keychain_access_groups(self):
        self.assertEqual(self.entitlements.keychain_access_groups[0], 'SPAMHAMEGG.*')
        self.assertEqual(len(self.entitlements.keychain_access_groups), 1)


if __name__ == '__main__':
    unittest.main()

