# Delimited

[![Build Status](https://travis-ci.org/chrisantonellis/delimited.svg?branch=master)](https://travis-ci.org/chrisantonellis/delimited) [![Coverage Status](https://coveralls.io/repos/github/chrisantonellis/delimited/badge.svg?branch=master)](https://coveralls.io/github/chrisantonellis/delimited?branch=master)

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
  # wow bummer
```
    
This is overly verbose and lacks the functionality needed to effectively interact with the data. Delimited provides classes that emulate native types and make accessing and modifying nested data easier. 

``` python
  from delimited import DelimitedDict as ddict
  
  mydict = ddict({
    "key1": {
      "key2": {
        "key3": "value"
      },
      "key4": ["value"]
    }
  })

  mydict.get("key1.key2.key3")
  # much better
```

Delimited provides `Path` classes to represent paths to nested data using tuples or strings, and `NestedContainer` classes that emulate the native `dict` and `collections.OrderedDict` types. Check out the [documentation](https://chrisantonellis.github.io/delimited/) to learn more.
