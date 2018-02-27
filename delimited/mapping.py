"""
delimited.mapping
~~~~~~~~~~~~~~~~~

This module defines NestedMapping objects. A NestedMapping object
implements an interface through which nested data can be accessed and
modified using Path objects.
"""

import copy

from delimited import NestedContainer

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath


class NestedMapping(NestedContainer):
    """ The abstract base class for NestedMapping objects. When subclassing
    NestedMapping the path and container attributes must be overridden with a
    Path object and container type respectively. The path object chosen defines
    the collapsed path format used by the NestedMapping class.
    """

    def __init__(self, *args, **kwargs):
        self.mapping = self.__class__
        super().__init__(*args, **kwargs)

    def __iter__(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield key, value

    def items(self):
        """ Yield key, value tuples for instance data.
        """

        for key, value in self.data.items():
            yield (key, value)

    def keys(self):
        """ Yield keys for instance data.
        """

        for key in self.data.keys():
            yield key

    def values(self):
        """ Yield values for instance data.
        """

        for value in self.data.values():
            yield value

    def update(self, data, path=None):
        """ Update instance data at path with data.
        """

        if isinstance(data, self.__class__):
            data = data.unwrap()

        self.ref(path).update(data)


class NestedDict(NestedMapping, dict):
    """ This class implements tuple path notation in use with the dict
    container type.
    """

    path = TuplePath
    container = dict
    
    def __init__(self, *args, **kwargs): # pragma: no cover
        from delimited.sequence import NestedList
        self.sequence = NestedList
        super().__init__(*args, **kwargs)


class DelimitedDict(NestedMapping, dict):
    """ This class implements delimited string path notation in use with the
    dict container type.
    """

    path = DelimitedStrPath
    container = dict
    
    def __init__(self, *args, **kwargs): # pragma: no cover
        from delimited.sequence import DelimitedList
        self.sequence = DelimitedList
        super().__init__(*args, **kwargs)
