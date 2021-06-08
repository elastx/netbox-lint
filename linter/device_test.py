"""Test for Netbox linting rules for Devices."""
# pylint: disable=C0116 (missing-function-docstring)
from collections import namedtuple
import unittest

from . import device as rules


class FakeDevice(namedtuple('FakeDevice', ['name'])):
    """A fake device replicating the Netbox Device model."""


class TestDeviceNamingRule(unittest.TestCase):
    """Tests the behavior of the DeviceNamingRule check."""

    def test_invalid_chars(self):
        rule = rules.DeviceNamingRule({})
        device = FakeDevice(name='Fake')
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Name contains invalid characters',
        ])

    def test_too_short_name(self):
        rule = rules.DeviceNamingRule({})
        device = FakeDevice(name='f1')
        got = list(rule.check(device))
        self.assertCountEqual(got, [
            'Name is too short',
        ])


if __name__ == '__main__':
    unittest.main()
