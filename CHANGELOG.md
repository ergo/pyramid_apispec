# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

<!--
   PRs should document their user-visible changes (if any) in the
   Unreleased section, uncommenting the header as necessary.
-->

<!-- ## Unreleased -->
<!-- ### Changed -->
<!-- ### Added -->
<!-- ### Removed -->
<!-- ### Fixed -->

## [0.4.0] - 2020-10-21
### Fixed
* API Explorer does not work when there are arguments on path [(#PR13)](https://github.com/ergo/pyramid_apispec/pull/13)
### Changed
* [Possibly breaking] Depends on APISpec >= 3.0.0
* [Possibly breaking] Swagger UI version 3.35.2

## [0.3.3] - 2019-05-12
### Added
* `route_args` and `view_args` params to `build_api_explorer_view` for more fine grained control
  of api-explorer view registration
### Changed
* [Possibly breaking] Depends on APISpec 1.3.3

## [0.3.2] - 2019-02-09
### Changed
* Depends on APISpec 1.0.0

## [0.3.1] - 2019-01-31
### Changed
* [Possibly breaking] Depends on APISpec 1.0.0rc1
### Fixed
* Handle cornice views better


## [0.3.0] - 2018-10-08
### Changed
* [Possibly breaking] Depends on APISpec 1.0.0b5


## [0.2.1] - 2018-08-11
### Fixed
* Handle routes with regex patterns better


## [0.2.0] - 2018-08-09
### Changed
* [Possibly breaking] Support and pin to ApiSpec >= 1.0.0b1
