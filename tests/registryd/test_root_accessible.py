# Pytest will pick up this module automatically when running just "pytest".
#
# Each test_*() function gets passed test fixtures, which are defined
# in conftest.py.  So, a function "def test_foo(bar)" will get a bar()
# fixture created for it.

import pytest
import dbus

PROPERTIES_IFACE = 'org.freedesktop.DBus.Properties'
ACCESSIBLE_IFACE = 'org.a11y.atspi.Accessible'

def get_property(proxy, iface_name, prop_name):
    return proxy.Get(iface_name, prop_name, dbus_interface=PROPERTIES_IFACE)

def test_accessible_iface_properties(registry_root, session_manager):
    values = [
        ('Name',        'main'),
        ('Description', ''),
        ('Parent',      ('', '/org/a11y/atspi/null')),
        ('ChildCount',  0),
    ]

    for prop_name, expected in values:
        assert get_property(registry_root, ACCESSIBLE_IFACE, prop_name) == expected

def test_unknown_property_yields_error(registry_root, session_manager):
    with pytest.raises(dbus.exceptions.DBusException):
        get_property(registry_root, ACCESSIBLE_IFACE, 'NonexistentProperty')