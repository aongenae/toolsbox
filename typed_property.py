#!/usr/bin/env python
from weakref import WeakKeyDictionary


class SlotsProperties(type):

    def __new__(meta, name, bases, dct):
        ''' Convert the class to use __slots__ instead of __dict__

            We also add __weakref__ if we inherit from object
            This enforces that the this type class must be used on a class that
            inheriting from 'object'
        '''
        dct['__slots__'] = []
        if object in bases:
            dct['__slots__'].append('__weakref__')
        return super(SlotsProperties, meta).__new__(meta, name, bases, dct)

    def __init__(cls, name, bases, dct):
        ''' We populate the __slots__ with the class variable
            these variables will be the only one allowed
        '''
        potential_slots = dct['__slots__']
        for element in dct:
            if isinstance(dct[element], TypedProperty):
                potential_slots.append(element)
        dct['__slots__'] = potential_slots
        super(SlotsProperties, cls).__init__(name, bases, dct)


class TypedProperty(object):

    __slots__ = ['_default', '_enforced_type', '_values', '__weakref__']

    def __init__(self, enforced_type, default=None):
        self._default = default
        self._enforced_type = enforced_type
        self._values = WeakKeyDictionary()
        if default is not None:
            self.__set__(self, default)

    def __get__(self, instance, owner):
        return self._values.get(instance, self._default)

    def __set__(self, instance, value):
        # rely on a function that can convert a string to a known class
        assert is_instance_of(value, self._enforced_type)
        self._values[instance] = value

    def __delete__(self, instance):
        del self._values[instance]
