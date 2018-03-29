"""
delimited.container
~~~~~~~~~~~~~~~~~
"""

import copy

from delimited.sequence import SequenceIndex
from delimited.sequence import SequenceValue
from delimited.exceptions import StopPathIteration


class NestedContainer(object):
    container = None
    path = None
    sequence = None
    mapping = None
    
    def __init__(self, data=None):
        self(data)
        
    def __call__(self, data=None):
        if data is None:
            self.data = self.container()
        elif issubclass(data.__class__, self.__class__):
            self.data = copy.deepcopy(data.data)
        elif isinstance(data, self.container):
            self.data = self._wrap(data)
        else:
            raise TypeError(f"data is not of type {self.container}")
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.data == other.data
        return self.data == other
        
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

    def clear(self):
        return self()

    def _wrap(self, data):
        if isinstance(data, (dict, list)):
            i = data.items() if isinstance(data, dict) else enumerate(data)
            
            for key, value in i:    
                if isinstance(value, dict):
                    data[key] = self.mapping(data[key])
                elif isinstance(value, list):
                    data[key] = self.sequence(data[key])
                
        return data
    
    def _unwrap(self, data):
        if isinstance(data, (self.mapping, self.sequence, dict, list)):
            i = data.items() if isinstance(data, dict) else enumerate(data)
            
            for key, value in i:
                if isinstance(value, (self.mapping, self.sequence)):
                    data[key] = value.get()
    
        return data
        
    def unwrap(self):
        return self._unwrap(self)

    def _access_handler(self, haystack, segment, path, i, kwargs={}):
        return haystack[segment], None

    def _access(self, path=None, create=False, _update_function=None, _update_kwargs={}):
    
        # setup haystack
        haystack = self.data
        status = None
    
        # setup path
        if not isinstance(path, self.path):
            path = self.path(path)
    
        # evaluate path
        for i, segment in enumerate(path):
    
            try:
                
                # handle segment
                if isinstance(segment, SequenceIndex):
                    s = segment.index
                else:
                    s = segment
                
                kwargs = {
                    "haystack": haystack,
                    "segment": s,
                    "path": path,
                    "i": i
                }    
                
                if i == len(path) - 1 and _update_function is not None:
                    function = _update_function
                    kwargs.update(_update_kwargs)
                    
                else:
                    function = self._access_handler
                    kwargs.update({
                        "kwargs": {
                            "create": create,
                            "_update_function": _update_function,
                            "_update_kwargs": _update_kwargs
                        }
                    })
                
                haystack, status = function(**kwargs)
    
            except StopPathIteration as e:
                haystack, status = e.get()
                break
    
            except (KeyError, IndexError) as e:
                
                if create:
                    
                    if isinstance(segment, SequenceIndex):
                        while len(haystack) < s + 1:
                            haystack.append(SequenceValue())
                    
                    if i == len(path) - 1:
                        
                        if _update_function is None or _update_function is self._set_handler:
                            if isinstance(segment, SequenceIndex):
                                haystack[s] = self.sequence()
                            else:
                                haystack[s] = self.mapping()    
                        
                        elif _update_function in [self._push_handler, self._pull_handler]:
                            haystack[s] = self.sequence()
                    
                    else:
                        if isinstance(path[i+1], SequenceIndex):
                            haystack[s] = self.sequence()
                        else:
                            haystack[s] = self.mapping()
                            
                    haystack, status = function(**kwargs)
                else:
                    # TODO: fix this, exceptions swallowing error from
                    # lower level exception
                    # e.args = (f"{s} in {path}",) + e.args[1:]
                    raise
    
            except TypeError as e:
                raise
        
        return haystack, status
        
    def ref(self, path=None, create=False):
        return self._access(path=path, create=create)[0]

    def get(self, path=None, *args):
        try:
            return copy.deepcopy(self._unwrap(self.ref(path)))
        except (KeyError, IndexError, TypeError):
            if args:
                return args[0]
            raise

    def has(self, path=None):
        try:
            return bool(self.ref(path))
        except (KeyError, IndexError, TypeError):
            return False



    def _set_handler(self, haystack, value, segment, path, i):
        haystack[segment] = value
        return None, None

    def set(self, path, value, create=True):
        haystack, status = self._access(
            path=path,
            create=create,
            _update_function=self._set_handler,
            _update_kwargs={"value": value}
        )



    def _unset_handler(self, haystack, segment, path, i):
        del haystack[segment]
        return None, None

    def unset(self, path):
        haystack, status = self._access(
            path=path,
            _update_function=self._unset_handler
        )


    def _push_handler(self, haystack, segment, path, i, value, create):
        if create == True and not isinstance(haystack[segment], self.sequence):
            haystack[segment] = [haystack[segment]]
        haystack[segment].append(value)
        return None, None


    def push(self, path, value, create=True):
        haystack, status = self._access(
            path=path,
            create=create,
            _update_function=self._push_handler,
            _update_kwargs={
                "value": value,
                "create": create
            }
        )

    def _pull_handler(self, haystack, segment, path, i, value, cleanup):
        haystack[segment].remove(value)
        if cleanup == True and len(haystack[segment]) == 0:
            del haystack[segment]
        return None, None

    def pull(self, path, value, cleanup=False):
        haystack, status = self._access(
            path=path,
            _update_function=self._pull_handler,
            _update_kwargs={
                "value": value,
                "cleanup": cleanup
            }
        )

    def copy(self, path=None):
        return copy.copy(self)

    def clone(self, path=None):
        clone = self.__class__()
        clone.data = self.ref(path)
        return clone
    
    @classmethod
    def _merge(cls, a, b):
        if not isinstance(a, b.__class__):
            return copy.copy(a)
        
        b = copy.copy(b)
        iterable = a.keys() if isinstance(a, dict) else range(len(a))
        
        for k in iterable:
            
            # sequences
            if all(isinstance(v, list) for v in [a, b]):
                
                # unequal lengths
                if k > (len(b) - 1):
                    b.append(a[k])
                
                # recursive merge
                else:
                    b[k] = cls._merge(a[k], b[k])
                    
            # mappings
            elif all(isinstance(v, dict) for v in [a, b]):
                
                # key not set
                if k not in b:
                    b[k] = a[k]
                
                # recursive merge
                else:
                    b[k] = cls._merge(a[k], b[k])
        
        return b
    
    def merge(self, data, path=None):
        
        if isinstance(data, self.__class__):
            data = data.get()
        
        return self._merge(self.get(path), data)
    
    def expand(self, data):
        self.data = self._expand(data)
        return self
    
    def _expand(self, data):
    
        # determine type for expanded data
        expanded = self.container()
    
        for path, value in data.items():
            if not isinstance(path, self.path):
                path = self.path(path)
    
            for i, segment in enumerate(reversed(path)):
    
                if isinstance(segment, SequenceIndex):
                    index = segment.index
                    new_segment = [SequenceValue()] * (index + 1)
    
                else:
                    index = segment
                    new_segment = dict()
    
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
        data = self if path is None else self.ref(path)
        return self._collapse(data, func=func)
    
    @classmethod
    def _collapse(cls, data, func=None, _parent_path=None):
        """ Recursively collapse expanded nested data and return.
        """

        collapsed = {}
        
        path = cls.path() if _parent_path is None else _parent_path

        # determine iterator
        if isinstance(data, cls.sequence):
            i, index = enumerate(data), cls.sequence.sequenceindex
        elif isinstance(data, cls.mapping):
            i, index = data.items(), None
        else:
            return data
            
        # capture func if already set on self
        if func is None and hasattr(cls, "_collapse_func"):
            func = cls._collapse_func

        for key, value in i:
            
            # NOTE: use of `func` results in current level not being collapsed
            if func is not None and func(key, value, data.__class__):

                if isinstance(data, cls.sequence):
                    uncollapsed = list([SequenceValue()] * (key + 1))
                    
                elif isinstance(data, cls.mapping):
                    uncollapsed = dict()

                # assign collapsed value to container
                # NOTE: by omitting `_parent_path` in collapse call below and 
                # assiging directly to container, all paths of collapsed
                # children will not include current level path
                uncollapsed[key] = cls._collapse(value, func=func)
                value = {path.encode(): uncollapsed} if len(path) else uncollapsed

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
                if not isinstance(value, (list, dict)) and len(path_copy):
                    value = {path_copy.encode(): value}

            # update root with branch
            collapsed = cls._merge(collapsed, value)
            # collapsed.update(value)

        return collapsed
