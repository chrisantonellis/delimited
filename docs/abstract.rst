Abstract
~~~~~~~~

Purpose
-------

:ref:`Nested data <nested_data>` can be easily expressed in python but not easily accessed or modified. Using builtin methods, accessing nested data requires chaining :func:`dict.get()` calls.

::
  
  mydict.get("exterior", {}).get("color", {}).get("trim", {}) # wow bummer
    
This is overly verbose and lacks the functionality needed to effectively interact with the data. **Delimited** provides classes that emulate native types and make accessing and modifying nested data easier. 

::
  
  mydict.get("exterior.color.trim") # much better

**Delimited** provides :py:class:`Path` classes to represent paths to nested data using tuples or strings, and :py:class:`NestedContainer` classes that emulate the native :class:`dict` type.

Terms
-----

.. _nested_data:

Nested data
^^^^^^^^^^^

Container type data that has other container types as values.

    ::
      
      {
        "key1": {
          "key2": {
            "key3": "value"
          }
        }
      }

.. _path:

Path
^^^^

An group of path segments that represent a location within a nested data structure.

  ::

    "key1.key2.key3"
    
  .. note::

    The example is using the collapsed path format of :class:`DelimitedStrPath`

.. _path_segment:

Path segment
^^^^^^^^^^^^

A single part of a path representing a single location or level in a nested data structure.

    ::
    
      DelimitedStrPath("key1.key2.key3")[1]
      
      # "key2"

.. _collapsed_path_format:

Collapsed path format
^^^^^^^^^^^^^^^^^^^^^

The type and format of a hashable iterable used by the :meth:`~Path._encode` and :meth:`~Path._decode` methods of :class:`Path` objects. This is specific to the implementation of each :class:`Path` subclass.

    **TuplePath**
    ::

        ("key1", "key2", "key3")

    **DelimitedStrPath**
    ::

        "key1.key2.key3"

.. _tuple_path_notation:

Tuple path notation
^^^^^^^^^^^^^^^^^^^

The collapsed path format of the :py:class:`TuplePath` class.

    ::

        ("key1", "key2", "key3")


.. _delimited_string_path_notation:

Delimited string path notation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The collapsed path format of the :py:class:`DelimitedStrPath` class.

    ::

        "key1.key2.key3"
