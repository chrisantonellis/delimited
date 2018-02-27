import abc
import copy

from delimited.index import SequenceIndex
from delimited.index import ListIndex
from delimited.value import SequenceValue


__version__ = "0.0.6"
__title__ = "delimited"
__summary__ = "Defines types that allow for accessing and modifying nested data"
__url__ = "https://github.com/chrisantonellis/delimited"
__author__ = "Christopher Antonellis"
__email__ = "christopher.antonellis@gmail.com"
__license__ = "MIT License"


class NestedContainer(abc.ABC, object):
    container = None
    path = None
    sequence = None
    mapping = None
    
    def __init__(self, data=None):
        self(data)
        
    def __call__(self, data=None):
        if data is None:
            self.data = self.container()
            
        elif isinstance(data, self.container):
            self.data = self._wrap(data)
        
        else:
            raise Exception(f"data is not of type {self.container}")
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        if isinstance(other, self.container):
            return self.data == other
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.data)
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.data})"
    
    def __hash__(self):
        return hash(str(self.data))

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return bool(len(self.data))
    
    def __contains__(self, value):
        return value in self.data
    
    def __getitem__(self, path):
        return self.ref(path)

    def __setitem__(self, path, value):
        self.set(path, value)

    def __delitem__(self, path):
        self.unset(path)

    def __copy__(self):
        new = self.__class__()
        new.data = copy.copy(self.data)
        return new

    def __deepcopy__(self, *args):
        new = self.__class__()
        new.data = copy.deepcopy(self.data)
        return new

    def _wrap(self, data):
        
        iterable = data.items() if isinstance(data, dict) else enumerate(data)
        
        for key, value in iterable:
            
            if isinstance(value, dict):
                data[key] = self.mapping(data[key])
                
            elif isinstance(value, list):
                data[key] = self.sequence(data[key])
                
        return data
        
    def _unwrap(self, data):
    
        iterable = data.items() if isinstance(data, dict) else enumerate(data)
    
        for key, value in iterable:
    
            if isinstance(value, (self.mapping, self.sequence)):
                data[key] = value.ref()
    
        return data
        
    def unwrap(self):
        return self._unwrap(self.data)

    def ref(self, path=None, create=False):
        """ Return a reference to nested data at path. If create is True and
        missing key(s) are encountered while trying to resolve path, create
        the missing key(s) using an instance of self.container as the value.
        """

        # all attributes
        if path is None:
            return self.data

        # setup haystack
        haystack = self.data

        # setup path
        if not isinstance(path, self.path):
            path = self.path(path)

        # for each segment
        for i, segment in enumerate(path):
            
            s = segment.index if isinstance(segment, SequenceIndex) else segment
            
            try:
                haystack = haystack[s]

            except KeyError as e:
                if create:
                    haystack[s] = self.container()
                    haystack = haystack[s]

                else:
                    e.args = (f"{s} in {path}",) + e.args[1:]
                    raise
            
            except IndexError as e:
                if create:
                    haystack.append(self.container())
                    haystack = haystack[s]

                else:
                    e.args = (f"{s} in {path}",) + e.args[1:]
                    raise

            except TypeError as e:
                e.args = (f"{s} in {path}",) + e.args[1:]
                raise

        return haystack

    def get(self, path=None, *args):
        """ Return a copy of nested data at path. First value of args is
        considered the default value, and if self.ref call raises a KeyError,
        the default value will be returned.
        """

        try:
            return copy.deepcopy(self._unwrap(self.ref(path)))
        except (KeyError, IndexError):
            if args:
                return args[0]
            raise

    def has(self, path=None):
        """ Return True if path can be resolved in instance data else False.
        """

        try:
            return bool(self.ref(path))
        except (KeyError, IndexError):
            return False

    def copy(self, path=None):
        """ Return a new instance of self with its data set to a deep copy of
        this instances data.
        """
        
        return copy.copy(self)

    def clone(self, path=None):
        """ Return a new instance of self with its data set to a reference of
        this instances data.
        """

        spawn = self.__class__()
        spawn.data = self.ref(path)
        return spawn
    
    @classmethod
    def _merge(cls, a, b):
        
        if not isinstance(a, b.__class__):
            return copy.copy(a)
        
        b = copy.copy(b)
        iterable = a.keys() if isinstance(a, dict) else range(len(a))
        
        for k in iterable:
            
            # unequal length sequences
            if isinstance(a, list) and k > (len(b) - 1):
                b.append(a[k])
            
            # mappings with key not set
            elif isinstance(a, dict) and k not in b:
                b[k] = a[k]
            
            # sequences and mappings
            else:
                b[k] = cls._merge(a[k], b[k])
        
        return b
    
    def merge(self, data, path=None):
        if isinstance(data, self.__class__):
            data = data.unwrap()
            
        return self._merge(data, self.get(path))
    
    def _expand(self, data):

        # determine type for expanded data
        expanded = self.container()

        for path, value in data.items():
            if not isinstance(path, self.path):
                path = self.path(path)

            for i, segment in enumerate(reversed(path)):

                if isinstance(segment, SequenceIndex):
                    index = segment.index
                    new_segment = self.sequence([SequenceValue()] * (index + 1))
                    
                else:
                    index = segment
                    new_segment = self.mapping()

                # first segment
                if i == 0:
                    new_segment[index] = value
                    expanded_segment = new_segment

                # > first segment
                elif i > 0:
                    new_segment[index] = expanded_segment
                    expanded_segment = new_segment

                # last segment
                if i == (len(path) - 1):
                    expanded = self._merge(expanded, expanded_segment)

        return expanded

    def collapse(self, path=None, func=None):
        """ Collapse instance data at path and return. Use func to determine
        if a level of nested data should be collapsed or not.
        """

        return self._collapse(self if path is None else self.get(path), func=func)
    
    @classmethod
    def _collapse(cls, data, func=None, _parent_path=None):
        """ Recursively collapse expanded nested data and return.
        """

        collapsed = {}
        path = _parent_path if _parent_path is not None else cls.path()

        # sequence
        if isinstance(data, list):
            iterable, index = enumerate(data), ListIndex

        # mapping
        elif isinstance(data, dict):
            iterable, index = data.items(), None

        # all others
        else:
            return data

        for key, value in iterable:
            
            # NOTE: use of `func` results in current level not being collapsed
            if callable(func) and func(key, value):

                if isinstance(data, list):
                    uncollapsed = list([SequenceValue()] * (key + 1))
                    
                elif isinstance(data, dict):
                    uncollapsed = dict()

                # assign collapsed value to container
                # NOTE: by omitting `_parent_path` in collapse call below and 
                # assiging directly to container, all paths of collapsed
                # children will not include current level path
                uncollapsed[key] = cls._collapse(value, func=func)
                value = {path.encode(): uncollapsed}

            else:

                # wrap key in sequence index class if necessary
                if index is not None:
                    key = index(key)

                # NOTE: create copy of path so further extend calls do not
                # mutate current level path
                path_copy = path.copy()
                path_copy.extend(key)

                # continue to collapse nested values
                value = cls._collapse(value, func=func, _parent_path=path_copy)

                # if value is not collapsable, tree has been traversed for branch
                # and value of `encoded path: value` should be returned
                if not isinstance(value, (list, dict)):
                    value = {path_copy.encode(): value}

            # update root with branch
            collapsed.update(value)

        return collapsed
    
    def set(self, path, value, create=True):
        """ Set value at path in instance data. If create is True, create
        missing keys while trying to resolve path.
        """

        if not isinstance(path, self.path):
            path = self.path(path)
            
        tail = path.tail
        if path.head is None and isinstance(path.tail, SequenceIndex):
            tail = path.tail.index
            
        haystack = self.ref(path.head, create=create)
        haystack[tail] = value

    def unset(self, path, cleanup=False):
        """ Remove value and last key at path. If cleanup is True and key
        removal results in empty container, remove empty container.
        """

        if not isinstance(path, self.path):
            path = self.path(path)
        
        haystack = self.ref(path.head)
        
        tail = path.tail
        if path.head is None and isinstance(path.tail, SequenceIndex):
            tail = path.tail.index
        
        del haystack[tail]

        if cleanup and path.head is not None:
            if not len(haystack):
                self.unset(path.head)

        return True

    def push(self, path, value, create=True):
        """ Push value to list at path in instance data. If create is True and
        key for final path segment is not set, create key and create value as
        empty list and append value to list. If create is True and key for
        final path segment is wrong type, create value as list with existing
        value and append value to list.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head, create=create)
        
        tail = path.tail
        if path.head is None and isinstance(path.tail, SequenceIndex):
            tail = path.tail.index

        try:
            haystack[tail].append(value)

        except KeyError as e:
            if create:
                haystack[tail] = self.sequence()
                haystack[tail].append(value)
            else:
                e.args = (f"{tail} in {path}",) + e.args[1:]
                raise

        except AttributeError as e:
            if create:
                haystack[tail] = self.sequence([haystack[tail]])
                haystack[tail].append(value)
            else:
                e.args = (f"{tail} in {path}",) + e.args[1:]
                raise

        return True

    def pull(self, path, value, cleanup=False):
        """ Remove value from list at path in instance data. If cleanup is True
        and removal of value results in an empty list, remove list and key.
        """

        if not isinstance(path, self.path):
            path = self.path(path)

        haystack = self.ref(path.head)

        tail = path.tail
        if path.head is None and isinstance(path.tail, SequenceIndex):
            tail = path.tail.index

        haystack[tail].remove(value)

        if cleanup:
            if not len(haystack[tail]):
                del haystack[tail]

        return True






# class NestedType(object):
# 
#     def __new__(cls, name, path):
# 
#         mapping = type(
#             f"{name.title()}Dict",
#             (NestedContainer,),
#             {
#                 "container": dict,
#                 "path": path
#             }
#         )
# 
#         sequence = type(
#             f"{name.title()}List",
#             (NestedContainer,),
#             {
#                 "container": list,
#                 "path": path,
#                 "index": ListIndex,
#             }
#         )
# 
# 
# NestedDict, NestedList = NestedType(TuplePath)