# Delimited 0.0.5

[![Travis](https://img.shields.io/travis/chrisantonellis/delimited.svg?style=flat-square)](https://img.shields.io/travis/USER/REPO.svg)
[![Coveralls github](https://img.shields.io/coveralls/github/chrisantonellis/delimited.svg?style=flat-square)](https://coveralls.io/github/chrisantonellis/delimited)
[![PyPI](https://img.shields.io/pypi/v/delimited.svg?style=flat-square)](https://pypi.python.org/pypi/delimited/0.0.5)
![Somethin](https://img.shields.io/badge/code%20style-pep8-brightgreen.svg?style=flat-square)

Delimited defines classes that allow for accessing and modifying nested data.

## Installation

```
pip install delimited
```

## Documentation

[https://chrisantonellis.github.io/delimited/](https://chrisantonellis.github.io/delimited/)

## Abstract

**Nested data** can be easily expressed in python but not easily accessed or modified. Using builtin methods, accessing nested data requires chaining `dict.get()` calls.
``` python
  mydict = {
    "key1": {
      "key2": {
        "key3": "value"
      }
    }
  }

  mydict.get("key1", {}).get("key2", {}).get("key3", {})
```
    
This is overly verbose and lacks the functionality needed to effectively interact with the data. Delimited provides classes that emulate native types and make accessing and modifying nested data easier. 

``` python
  from delimited import DelimitedDict as ddict
  
  mydict = ddict({
    "key1": {
      "key2": {
        "key3": "value"
      }
    }
  })

  mydict.get("key1.key2.key3")
  # returns "value"
  
  mydict.collapse()
  # returns {"key1.key2.key3": "value"}
```

Delimited provides `Path` classes to represent paths to nested data using tuples or strings, and `NestedContainer` classes that emulate the native `dict` and `collections.OrderedDict` types. Check out the [documentation](https://chrisantonellis.github.io/delimited/) to learn more.
