#!/usr/bin/env python
from ..typed_property import SlotsProperties, TypedProperty
from future.utils import with_metaclass
import unittest


class DummyInstance(object):

    def __init__(self):
        pass


class Dummy(with_metaclass(SlotsProperties, object)):

    boolean_default_none = TypedProperty('bool')
    boolean_default_true = TypedProperty('bool', True)
    boolean_default_false = TypedProperty('bool', False)
    boolean_init = TypedProperty('bool')
    boolean_default_true_init_false = TypedProperty('bool', True)
    dummy_instance_parent = TypedProperty('DummyInstance')

    def __init__(self, boolean_init=True, boolean_default_true_init_false=False):
        self.boolean_init = boolean_init
        self.boolean_default_true_init_false = boolean_default_true_init_false


class DummyChild(Dummy):
    ''' This class will inherit the metaclass '''

    dummy_instance_init = TypedProperty('DummyInstance')
    dummy_instance_child = TypedProperty('DummyInstance')

    def __init__(self, dummy_instance_init=None):
        super(DummyChild, self).__init__(
            boolean_init=False,                       # we change boolean_init !
            boolean_default_true_init_false=False
        )
        self.dummy_instance_init = dummy_instance_init


class TestTypedProperty(unittest.TestCase):

    def setUp(self):
        self.dummy = Dummy()

    def test_boolean_default_none(self):
        # In TypedProperty, the absence of explicit default fall back to None
        self.assertIsNone(self.dummy.boolean_default_none)

    def test_boolean_default_none_assign(self):
        self.dummy.boolean_default_none = True
        self.assertTrue(self.dummy.boolean_default_none)

    def test_boolean_default_true(self):
        self.assertTrue(self.dummy.boolean_default_true)

    def test_boolean_init(self):
        self.assertTrue(self.dummy.boolean_init)

    def test_boolean_default_true_init_false(self):
        self.assertFalse(self.dummy.boolean_default_true_init_false)

    def test_cannot_add_property_outside_class_typed_property(self):
        with self.assertRaises(AttributeError):
            self.dummy.new_boolean = None

    def test_builtin_type_enforced(self):
        with self.assertRaises(AssertionError):
            self.dummy.boolean_default_none = 'not a boolean'

    def test_class_type_enforced(self):
        with self.assertRaises(AssertionError):
            self.dummy.dummy_instance_parent = 'not a boolean'


class TestTypedPropertyInheritance(TestTypedProperty):
    # Every test_* from TestTypedProperty will be rerun on our child class

    def setUp(self):
        self.dummy = DummyChild(DummyInstance())

    def test_boolean_init(self):
        # we override this test as the DummyChild has a different boolean_init
        self.assertFalse(self.dummy.boolean_init)

    def test_dummy_instance_init(self):
        self.assertIsInstance(self.dummy.dummy_instance_init, DummyInstance)

    def test_dummy_instance_child_default(self):
        self.assertIsNone(self.dummy.dummy_instance_child)

    def test_dummy_instance_child_assign(self):
        self.dummy.dummy_instance_child = DummyInstance()
        self.assertIsInstance(self.dummy.dummy_instance_child, DummyInstance)
