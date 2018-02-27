"""
delimited.sequence
~~~~~~~~~~~~~~~~~~

This module defines...
"""

import abc
import copy

from delimited import NestedContainer

from delimited.index import ListIndex
from delimited.path import TuplePath
from delimited.path import DelimitedStrPath


class NestedSequence(NestedContainer):
    index = None
        
    def __init__(self, *args, **kwargs):
        self.sequence = self.__class__
        super().__init__(*args, **kwargs)
        
    def __add__(self, other):
        self.data = self.data + self.container(other)
        
    def __iadd__(self, other):
        return self.__add__(other)
        
    def __iter__(self):
        for v in self.data:
            yield v
        
    def __reversed__(self):
        for v in self.data[::-1]:
            yield v
        
    def append(self, value):
        return self.data.append(value)
        
    def extend(self, data):
        if isinstance(data, self.__class__):
            data = data.data
        return self.data.extend(data)
        
    def insert(self, i, value):
        return self.data.insert(i, value)
        
    def remove(self, value):
        return self.data.remove(value)
        
    def pop(self, *args):
        return self.data.pop(*args)
        
    def clear(self):
        return self()
        
    def index(self, value):
        return self.data.index(value)
        
    def count(self, value):
        return self.data.count(value)
        
    def reverse(self):
        self.data = self.data[::-1]


class NestedList(NestedSequence, list):
    container = list
    index = ListIndex
    path = TuplePath
    
    def __init__(self, *args, **kwargs):
        from delimited.mapping import NestedDict
        self.mapping = NestedDict
        super().__init__(*args, **kwargs)
    

class DelimitedList(NestedSequence, list):
    container = list
    index = ListIndex
    path = DelimitedStrPath
    
    def __init__(self, *args, **kwargs):
        from delimited.mapping import DelimitedDict
        self.mapping = DelimitedDict
        super().__init__(*args, **kwargs)
