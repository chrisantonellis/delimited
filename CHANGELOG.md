# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## Unreleased

### Added
* Custom message injected into `KeyError`, `TypeError`, `AttributeError`

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
