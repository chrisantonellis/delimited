API
===


delimited.path
--------------

This module defines Path objects which are used to define :ref:`paths <path>` to :ref:`nested data <nested_data>` using one or more :ref:`path segments <path_segment>`.


Path
^^^^

.. py:class:: Path(value=None)

  The abstract base class for Path objects.

  .. py:method:: _encode(value)
  
    Abstract method. Encode value to :ref:`collapsed path format <collapsed_path_format>` and return.
    
    :param value: The value to encode
    :type value: list
    :returns: Encoded value
    :rtype: Value in :ref:`collapsed path format. <collapsed_path_format>`
    
  .. py:method:: _decode(value)

    Abstract method. Decode value in :ref:`collapsed path format <collapsed_path_format>` format to a list and return.
    
    :param value: The value to decode
    :returns: Decoded value
    :rtype: list


DelimitedStrPath
^^^^^^^^^^^^^^^^

.. py:class:: DelimitedStrPath(value=None)

  This class implements :ref:`delimited string path notation <delimited_string_path_notation>` as its :ref:`collapsed path format <collapsed_path_format>`.
  
  ::
    
    "key1.key2.key3"

  .. py:attribute:: segments
  
    A list where this instances path segments are stored.

  .. py:method:: _encode(value)

    Encode value to :ref:`collapsed path format <collapsed_path_format>` and return.
    
    :param value: The value to encode
    :type value: list
    :returns: Encoded value
    :rtype: Value in :ref:`collapsed path format <collapsed_path_format>`
    
    ::
      
      mypath = DelimitedStrPath()
      mypath._encode(["key1", "key2", "key3"])
      # returns "key1.key2.key3"

  .. py:method:: _decode(value)

    Decode value in :ref:`collapsed path format <collapsed_path_format>` to list and return.
    
    :param value: The value to decode
    :returns: Decoded value
    :rtype: list
    
    ::
      
      mypath = DelimitedStrPath()
      mypath._decode("key1.key2.key3")
      # returns ["key1", "key2", "key3"]

  .. py:method:: append(value)

    Add value to the end of :attr:`segments`. Accepts a :ref:`path segment <path_segment>`.
    
    :param value: The value to append
    
    ::
      
      mypath = DelimitedStrPath("key1.key2")
      mypath.append("key3")
      print(mypath)
      # prints "key1.key2.key3"

  .. py:method:: extend(values)

    Add each item of values to the end of :attr:`segments`. Accepts an instance of self or a encoded group of :ref:`path segments <path_segment>`.
    
    :param value: The values to extend with
    
    ::
      
      mypath = DelimitedStrPath("key1.key2")
      mypath.extend("key3.key4")
      print(mypath)
      # prints "key1.key2.key3.key4"

  .. py:method:: insert(i, value)

    Insert value at index i in :attr:`segments`.
    
    :param value: The value to insert
    :param i: The index at which to insert
    :type i: int
    
    ::
      
      mypath = DelimitedStrPath("key1.key3")
      mypath.insert(1, "key2")
      print(mypath)
      # prints "key1.key2.key3"

  .. py:method:: remove(value)

    Remove the first item from :attr:`segments` that is equal to value. Raise an exception if value is not found.
    
    :param value: The value to remove
    :raises: AttributeError
    
    ::
      
      mypath = DelimitedStrPath("root.key1.key2.key3")
      mypath.remove("root")
      print(mypath)
      # prints "key1.key2.key3"

  .. py:method:: pop(*args)

    Remove the item at index i from :attr:`segments` and return.
    
    :param i: The index from which to remove
    :type i: int
    :returns: Value at index i in :attr:`segments`
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.pop(1)
      # returns "key2"
      
      print(mypath)
      # prints "key1.key3"
      
    If i is not given, remove and return the first value from :attr:`segments`.
      
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.pop()
      # returns "key1"
      
      print(mypath)
      # prints "key2.key3"
    
    :returns: First value from :attr:`segments`
  
  .. py:method:: clear()

    Remove all values from :attr:`segments`.
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.clear()
      print(mypath)
      # prints ""

  .. py:method:: index(value)

    Return the index of the first item that is equal to value in :attr:`segments`. Raise an exception if value is not found.
    
    :param value: The value to search for
    :returns: The index at which the value was found
    :rtype: int
    :raises: AttributeError
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.index("key2")
      # returns 1

  .. py:method:: count(value)

    Return the number of times value appears in :attr:`segments`.
    
    :param value: The value to count for
    :returns: The count of value from :attr:`segments`
    :rtype: int
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.index("key1")
      # returns 1

  .. py:method:: reverse()

    Reverse :attr:`segments` in place.
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.reverse()
      print(mypath)
      # prints "key3.key3.key1"

  .. py:method:: copy()

    Return an instance of :py:class:`DelimitedStrPath` with its :attr:`segments` set to a copy of this instances :attr:`segments`.
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.copy()
      # returns instance of DelimitedStrPath
      
  .. py:method:: clone()
  
    Return an isntance of :py:class:`DelimitedStrPath` with its :attr:`segments` set to a reference to this instances :attr:`segments`.
    
    ::
      
      mypath1 = DelimitedStrPath("key1.key2.key3")
      mypath2 = mypath1.clone()
      mypath2[1] = "foo"
      print(mypath1)
      
      # returns "key1.foo.key3"

  .. py:method:: encode()

    Call :meth:`_encode` with :attr:`segments` as the values keyword argument and return.
    
    ::
      
      mypath = DelimitedStrPath("key1.key2.key3")
      mypath.encode()
      # returns "key1.key2.key3"
    
      
TuplePath
^^^^^^^^^

.. py:class:: TuplePath(value)

  This class implements :ref:`tuple path notation <tuple_path_notation>` as its collapsed path format.
  
  ::
    
    ("key1", "key2", "key3")
    
    
  TuplePaths can handle any hashable type as a :ref:`path segment <path_segment>`. All methods except for :meth:`_encode` and :meth:`_decode` are the same as :class:`DelimitedStrPath` as they both inherit from :class:`Path`.
  
  .. py:method:: _encode(value)
  
    Encode a list to :ref:`collapsed path format <collapsed_path_format>` and return.
    
    ::
      
      TuplePath._encode(["key1", "key2", "key3"])
      # returns ("key1", "key2", "key3")
      
    :param value: The value to encode
    :type value: list
    :returns: Encoded value
    :rtype: Value in :ref:`collapsed path format. <collapsed_path_format>`
    
  .. py:method:: _decode(value)
  
    Decode :ref:`collapsed path format <collapsed_path_format>` format to a list and return.
    
    ::
      
      TuplePath._encode(("key1", "key2", "key3"))
      # returns ["key1", "key2", "key3"]
      
    :param value: The value to decode
    :returns: Decoded value
    :rtype: list


delimited.container
-------------------

This module defines NestedContainer objects. A NestedContainer object implements an interface through which nested data can be accessed and modified.


NestedContainer
^^^^^^^^^^^^^^^

.. py:class:: NestedContainer(data=None)

  The abstract base class for NestedContainer objects. The path and container attributes must be overridden when subclassing.

  .. py:attribute:: path
  
    The :py:class:`Path` class used by this NestedContainer.
    
  .. py:attribute:: container
  
    The container type that this NestedContainer emulates.


DelimitedDict
^^^^^^^^^^^^^

.. py:class:: DelimitedDict(data=None)
  
  This class implements :ref:`delimited string path notation <delimited_string_path_notation>` in use with the dict container type.
  
  .. py:attribute:: path
    
    Set to :class:`DelimitedStrPath`
    
  .. py:attribute:: container
  
    Set to dict
    
  .. py:attribute:: data
  
    Instance data
  
  .. py:method:: _merge(a, b)
  
    Recursively merge container a into a copy of container b, overwriting values from b if conflicts are found.
    
    :param a: Container to merge from
    :type a: dict
    :param b: Container to merge into
    :type b: dict
    :returns: Merged data
    :rtype: boolean
    
    ::
      
      data_1 = {
        "key1": "value1",
        "key2": "value1" # conflict
      }
      
      data_2 = {
        "key2": "value2", # conflict
        "key3": "value2",
      }
      
      mycontainer = DelimitedDict()
      mycontainer._merge(data_2, data_1)
      
      # returns {
      #   "key1": "value1",
      #   "key2": "value2",
      #   "key3": "value2"
      # }

  .. py:method:: _expand(data)
  
    Recursively expand collapsed nested data and return.
    
    :param data: The data to expand
    :type data: dict
    :returns: Expanded data
    :rtype: dict
    
    ::
      
      data = {
        "key1.key2": {
          "key3": "value"
        }
      }
      
      mycontainer = DelimitedDict()
      mycontainer._expand(data)
      
      # returns {
      #   "key1": {
      #     "key2": {
      #       "key3": "value"
      #     }
      #   }
      # }

  .. py:method:: _collapse()
  
    Recursively collapse nested data and return. The param ``func`` should accept two params, ``key`` and ``value`` which will be the key of the current level of nested data being collapsed and the value of that key respectively.
    
    :param data: The nested data to collapse
    :type data: dict
    :param func: A function used to determine whether to collapse a level of nested data
    :type func: function
    :returns: Collapsed data
    :rtype: dict
    
    ::
      
      data = {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }
      
      mycontainer = DelimitedDict()
      mycontainer._collapse(data)
      
      # returns {
      #   "key1.key2.key3": "value"
      # }
      
      def should_collapse(path, value):
        if path == "key3":
          return False
        return True
        
      mycontainer._collapse(data, func=should_collapse)
      
      # returns {
      #   "key1.key2": {
      #     "key3": "value"
      #   }
      # }

  .. py:method:: items()
  
    Yield key, value tuple for values in :attr:`data`

  .. py:method:: keys()
  
    Yield keys for keys in :attr:`data`

  .. py:method:: values()
    
    Yield values for values in :attr:`data`

  .. py:method:: ref(path=None, create=False)
  
    Return a reference to nested data at path. If create is True and missing key(s) are encountered while trying to resolve path, create the missing key(s) using an instance of self.container as the value.
    
    :param path: The path to resolve
    :type path: str
    :param create: If True, create missing key(s)
    :type create: boolean
    
    ::
      
      data = {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }
      
      mycontainer = DelimitedDict(data)
      mycontainer.ref("key1.key2")
      
      # returns {
      #   "key3": "value"
      # }

  .. py:method:: get(path=None, *args)
  
    Return a copy of nested data at path. First value of args is considered the default value, and if the internal :meth:`ref` call raises a KeyError, the default value will be returned.
    
    :param path: The path to resolve
    :type path: str
    :param args[0]: Default value
    
    ::
      
      data = {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }
      
      mycontainer = DelimitedDict(data)
      mycontainer.ref("key1.key2")
      
      # returns {
      #   "key3": "value"
      # }

  .. py:method:: has(path=None)
  
    Return True if path can be resolved in :attr:`data` else False.
    
    :param path: The path to resolve
    :type path: str
    :rtype: boolean
    
    ::
      
      data = {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }
      
      mycontainer = DelimitedDict(data)
      mycontainer.has("key1.key2")
      # returns True
      
      mycontainer.has("foo")
      # returns False

  .. py:method:: copy(path=None)
  
    Return a new instance of self with its :attr:`data` set to a deep copy of this instances :attr:`data`.
    
    :param path: The path to resolve
    :type path: str
    :returns: New instance with copied data
    :rtype: :class:`DelimitedDict`
    
    ::
      
      mycontainer = DelimitedDict({"key": "value"})
      mycontainer.copy()
      
      # returns instance of DelimitedDict

  .. py:method:: clone()
  
    Return a new instance of self with its :attr:`data` set to a reference of this instances :attr:`data`.
    
    :rtype: instance of :class:`DelimitedDict`
    
    ::
      
      mycontainer = DelimitedDict({"key": "value"})
      mycontainer.clone()
      
      # returns instance of DelimitedDict

  .. py:method:: merge(data, path=None)
    
    Merge data with a copy of :attr:`data` at path and return merged data. Will accept instance of :class:`DelimitedDict` or instance of :attr:`container`.
    
    :param data: The data to merge
    :type data: dict
    :param path: The path at which to merge the data
    :type path: str
    :returns: The merged data
    :rtype: dict
    
    ::
      
      mycontainer = DelimitedDict({"key1": "value"})
      mycontainer.merge({"key2": "value"})
      
      # returns {
      #   "key1": "value",
      #   "key2": "value"
      # }

  .. py:method:: collapse(path=None, func=None)
  
    Collapse :attr:`data` at path and return. Use func to determine if a level of nested data should be collapsed.
    
    :param path: The path to resolve
    :type path: str
    :param func: The callable to use
    :type func: callable
    :returns: The collapsed data
    :rtype: dict
    
    ::
      
      data = {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }
      
      mycontainer = DelimitedDict(data)
      mycontainer.collapse("key1")
      
      # returns {
      #   "key2.key3": "value"
      # }

  .. py:method:: update(data, path=None)
  
    Update :attr:`data` at path with data.
    
    :param data: The data to use
    :type data: dict
    :param path: The path at which to update
    :type path: str
    
    ::
      
      mycontainer = DelimitedDict({"key1": "value"})
      mycontainer.update({"key2": "value"})
      mycontainer.get()
      
      # returns {
      #   "key1": "value",
      #   "key2": "value"
      # }

  .. py:method:: set(path, value, create=True)
  
    Set value at path in :attr:`data`. If create is True, create missing keys while trying to resolve path.
    
    :param path: The path to resolve
    :type path: str
    :param value: The value to set
    :param create: If True, create keys while resolving path
    :type create: boolean
    
    ::
      
      mycontainer = DelimitedDict()
      mycontainer.set("key", "value")
      mycontainer.get()
      
      # returns {"key": "value"}

  .. py:method:: push(path, value, create=True)
  
    Push value to list at path in :attr:`data`. If create is True and key for final path segment is not set, create key and create value as empty list and append value to list. If create is True and key for final path segment is wrong type, create value as list with existing value and append value to list.
    
    :param path: The path to resolve
    :type path: str
    :param value: The value to append
    :param create: If True, create list and append
    :type create: boolean
    
    ::
      
      mycontainer = DelimitedDict({"key": []})
      mycontainer.push("key", "value")
      mycontainer.get()
      
      # returns {"key": ["value"]}

  .. py:method:: pull(path, value, cleanup=False)
  
    Remove value from list at path in :attr:`data`. If cleanup is True and removal of value results in an empty list, remove list and key.
    
    :param path: The path to resolve
    :type path: str
    :param value: The value to pull
    :param cleanup: If True, remove empty list and key
    :type cleanup: boolean
    
    ::
      
      mycontainer = DelimitedDict({"key": ["value"]})
      mycontainer.push("key", "value")
      mycontainer.get()
      
      # returns {"key": []}

  .. py:method:: unset(path, cleanup=False)
  
    Remove value and last key at path. If cleanup is True and key removal results in empty container, recursively remove empty containers in reverse order of path.
    
    :param path: The path to resolve
    :type path: str
    :param cleanup: If True, recursively remove empty containers
    :type cleanup: boolean
    
    ::
      
      mycontainer = DelimitedDict({"key": "value"})
      mycontainer.unset("key")
      mycontainer.get()
      
      # returns {}

NestedDict
^^^^^^^^^^

.. py:class:: NestedDict(data=None)
  
  This class implements :ref:`tuple path notation <tuple_path_notation>` in use with the ``dict`` container type.
