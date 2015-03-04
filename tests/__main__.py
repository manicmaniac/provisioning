#!/usr/bin/env python
# -*- coding:utf-8 -*-

import unittest
import sys
import os.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from profile_test import ProvisioningProfileTests
from entitlements_test import EntitlementsTests

if __name__ == '__main__':
    unittest.main()

