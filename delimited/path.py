"""
delimited.path
~~~~~~~~~~~~~~

This module defines Path objects. a Path object implements an interface though
which a path to nested data can be defined using one or more path segments.
"""

import abc
import copy


class Path(abc.ABC):
    """ The abstract base class for Path objects. When subclassing Path the
    _encode and _decode methods must be overridden to handle an external 
    representation. Path segments are stored internally in a list in the
    segments attribute.
    """

    def __init__(self, path=None):
        self(path)

    def __call__(self, path=None):
        """ Overwrite path segments with decoded path param.
        If path param is None, set path segments to an empty list.
        """

        self.segments = self._decode(path) if path is not None else []

    def __add__(self, other):
        """ Add other to the end of path segments. Accepts a path segment.
        """

        self.segments = self.segments + [other]
        return self

    def __iadd__(self, other):
        """ Add other to the end of path segments. Accepts a path segment.
        """
        
        return self.__add__(other)

    def __eq__(self, other):
        """ Compare equality with instance of self or path in external 
        representation format.
        """

        if isinstance(other, self.__class__):
            value = self.segments == other.segments
        else:
            value = self.encode() == other
        return value

    def __ne__(self, other):
        """ Compare inequality with instance of self or path in external 
        representation format.
        """
        
        return not self.__eq__(other)

    def __hash__(self):
        """ Return hash of self.encode().
        """
        
        return hash(self.encode())

    def __len__(self):
        """ Return length of path segments.
        """
        
        return len(self.segments)

    def __bool__(self):
        """ Return length of path segments cast to boolean.
        """
        
        return bool(len(self.segments))

    def __str__(self):
        """ Return self.encode() cast to str.
        """
        
        return str(self.encode())

    def __repr__(self):
        """ Return class name joined with encoded path segments cast to str.
        """
        
        return "{}({})".format(self.__class__.__name__, self.encode())

    def __iter__(self):
        """ Yield path segments.
        """
        
        for k in self.segments:
            yield k

    def __reversed__(self):
        """ Yield path segments in reverse order.
        """
        
        for k in self.segments[::-1]:
            yield k

    def __contains__(self, key):
        """ Return boolean for presence of key in internal path segments. Accepts path segment.
        """
        
        return key in self.segments

    def __getitem__(self, i):
        """ Return item at index or slice in external representation format.
        """
        
        value = self.segments[i]
        if isinstance(value, list):
            value = self._encode(value)
        return value

    def __setitem__(self, i, value):
        """ Set item at index to value.
        """
        self.segments[i] = value

    def __delitem__(self, i):
        """ Delete item at index.
        """
        
        del self.segments[i]

    @classmethod
    @abc.abstractmethod
    def _encode(self, value):
        """ Encode list to external representation. This method must be 
        overridden when subclassing.
        """
        
        pass # pragma: no cover

    @classmethod
    @abc.abstractmethod
    def _decode(self, value):
        """ Decode a value in external representation format to a list. This 
        method must be overridden when subclassing.
        """
        
        pass # pragma: no cover
    
    @property
    def head(self):
        """ Return the head of the list of path segments, meaning all segments 
        except for the last one. If there is only one segment return None
        """
        
        return self.segments[:-1] if len(self.segments) > 1 else None

    def append(self, value):
        """ Add value to the end of path segments. Accepts a path segment.
        """

        return self.segments.append(value)

    def extend(self, values):
        """ Add each item of values to the end of path segments. Accepts an 
        instance of self or a encoded group of path segments.
        """

        if isinstance(values, self.__class__):
            values = values.segments
        else:
            values = self._decode(values)

        return self.segments.extend(values)

    def insert(self, i, value):
        """ Insert value at index i in path segments.
        """

        self.segments.insert(i, value)

    def remove(self, value):
        """ Remove the first item from path segments that is equal to value. 
        Raise an exception if value is not found.
        """

        return self.segments.remove(value)

    def pop(self, *args):
        """ Remove the item at index i from path segments and return. If i is 
        not given, remove and return the first value in self.segments.
        """

        return self.segments.pop(*args)

    def clear(self):
        """ Remove all values from path segments.
        """
        
        self()

    def index(self, value):
        """ Return the index from path segments of the first item that is 
        equal to value. Raise an exception if value is not found.
        """
        
        return self.segments.index(value)

    def count(self, value):
        """ Return the number of times value appears in path segments.
        """

        return self.segments.count(value)

    def reverse(self):
        """ Reverse path segments in place
        """

        self.segments = self.segments[::-1]

    def copy(self):
        """ Return an instance of self.__class__ with its path segments 
        set to a shallow copy of this instances path segments.
        """

        return copy.copy(self)

    def encode(self):
        """ Call self._encode with path segments and return result.
        """

        return self._encode(self.segments)


class TuplePath(Path):
    """ This class implements tuple path notation as its external 
    representation. TuplePaths can handle any hashable type as a path segment.
    Example: ("key1", "key2", "key3")
    """

    @classmethod
    def _encode(self, value):
        """ Encode a list to external representation format.
        """
        
        return tuple(value)

    @classmethod
    def _decode(self, value):
        """ Decode external representation format to a list.
        """
        
        return list(value) if isinstance(value, tuple) else [value]


class DelimitedStrPath(Path):
    """ This class implements delimited string path notation as its 
    external representation.
    Example: "key1.key2.key3"
    """

    delimiter = "."

    @classmethod
    def _encode(self, value):
        """ Encode a list to external representation format.
        """
        
        return self.delimiter.join(value)

    @classmethod
    def _decode(self, value):
        """ Decode external representation format to a list.
        """
        
        return value.split(self.delimiter)
