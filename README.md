### Delimited

#### Installation

```
pip install delimited
```

#### Documentation

[https://chrisantonellis.github.io/delimited/](https://chrisantonellis.github.io/delimited/)

#### About

**Nested data** can be easily expressed in python but not easily accessed or modified. Using builtin methods, accessing nested data requires chaining `dict.get()` calls.

```
  mydict.get("exterior", {}).get("color", {}).get("trim", {})
  # wow bummer
```
    
This is overly verbose and lacks the functionality needed to effectively interact with the data. **Delimited** provides classes that emulate native types and make accessing and modifying nested data easier. 

```
  mydict.get("exterior.color.trim")
  # much better
```

**Delimited** provides `Path` classes to represent paths to nested data using tuples or strings, and `NestedContainer` classes that emulate the native `dict` and `collections.OrderedDict` types.
