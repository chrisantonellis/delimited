# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [ 0.0.13 ] 2018-03-19

### Added
* `clear` method moved from `NestedSequence` to `NestedContainer` to allow 
  mapping and sequences types access to this method

## [ 0.0.12 ] 2018-03-19

### Changed
* `NestedContainer.__call__` changed to accept instance of self for data
  on instantiation, test case

## [ 0.0.11 ] 2018-03-19

### Changed
* `NestedContainer._wrap` method changed to handle non dict, list arg
* `NestedContainer._unwrap` method changed to handle also mapping, items arg
  
### Added
* `NestedContainer._collapse` now checks for existence of `_collapse_func` on 
  self and uses that if set, test case

## [ 0.0.10 ] 2018-03-16

### Changed
* fixed bug introduced to `NestedContainer._collapse` method

## [ 0.0.9 ] 2018-03-16

### Added
* returned to 100% test coverage
* `NestedContainer._expand` method and tests

### Changed
* fixed bug introduced to `NestedContainer._collapse` method

## [ 0.0.8 ] 2018-03-15

### Changed
* cleanup, removed unnecessary comments
* changed arguments passed to collapse function to `key`, `value`, `container`

## [ 0.0.7 ] 2018-03-08

### Added
* Custom message injected into `KeyError`, `TypeError`, `AttributeError`
* Support for nested sequences
  * SequenceIndex, ListIndex types
  * SequenceValue type
  * NestedSequence, NestedList types
* NestedType metaclass

## [ 0.0.6 ] 2018-01-06

### Added
* More badges added to `README.md`

### Changed
* `spawn` method renamed to `clone` in `NestedContainer` class
* `clone` method renamed to `copy` in `NestedContainer` class
* `clone` method added to `Path` class
* docs updated to reflect changes

## [ 0.0.5 ] 2018-01-05

### Added

* `value` added to `func` param in `NestedContainer._collapse` method
* fixed errors in docs

## [ 0.0.4 ] 2018-01-05

### Changed
* `travis.yml` to actually work
* tests updated to 100% passing
* custom `__repr__` method added to `DelimitedStrPath`

## [ 0.0.3 ] 2018-01-01

### Added
* `travis.yml`

### Changed
* bugfix for `DelimitedStrPath` added `path.head` property
* `__repr__` for `Path` classes fixed, missing single quotes

## [ 0.0.2 ] 2018-01-01

### Added
* **Documentation!**
* `func` param to `NestedContainer._collapse` and `NestedContainer.collapse` methods
* Dockerfile & docker-compose.yml file for isolated testing and dev

## [ 0.0.1 ] 2017-10-12

### Added
* initial release, sniping the name on pip
