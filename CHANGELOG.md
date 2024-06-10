## Latest changes

* Fix: tasks.repeat_every() and related tests [#305](https://github.com/dmontagu/fastapi-utils/issues/305)
* Fix typo [#306](https://github.com/dmontagu/fastapi-utils/issues/306)
* Merge with [fastapi-utils](https://github.com/dmontagu/fastapi-utils)

## 0.6.0

* Fix bug where `Request.url_for` is not working as intended [[yuval9313/FastApi-RESTful#90](https://github.com/yuval9313/FastApi-RESTful/issues/90)]
* Update multiple dependencies using @dependebot
* Fix `repeat_every` is only running once [#142](https://github.com/yuval9313/FastApi-RESTful/pull/142)

## 0.5.0

* Bump sqlalchemy from 1.4.48 to 2.0.19 by @dependabot in #202
* Pydantic v2 by @ollz272 in [#199](https://github.com/yuval9313/FastApi-RESTful/pull/199)
* fix ci not run by @ollz272 in [#208](https://github.com/yuval9313/FastApi-RESTful/pull/208)

## 0.4.5

* Change the lock of fastapi to enable more versions of it to be installed

## 0.4.4

* Move to ruff for linting, etc.
* Update various dependencies
* Stop supporting Python 3.6
* Deprecate InferringRouter (as its functionality is now built into `fastapi.APIRouter`)
* Resolve various deprecationwarnings introduced by sqlalchemy 1.4.
* Add support to Python 3.11
* Change package description to avoid errors with pypi as [mentioned here](https://github.com/yuval9313/FastApi-RESTful/issues/175)

## 0.4.3

* Fix bug where inferred router raises exception when no content is needed but type hint is provided (e.g. `None` as return type with status code 204) (As mentiond in [#134](https://github.com/yuval9313/FastApi-RESTful/pull/134))
* Improve tests and add more test cases
* Bump dependencies versions

## 0.4.2

* Remove version pinning to allow diversity in python environments

## 0.4.1

* Add more pypi classifiers

## 0.4.0

** Breaking change **
* Remove support to python < 3.6.2

Additionals:
* Multiple version bumps
* Add usage of **kwargs for to allow more options when including new router

## 0.3.1

* [CVE-2021-29510](https://github.com/samuelcolvin/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh) fix of pydantic - update is required
* Made sqlalchemy as extras installs 

## 0.3.0

* Add support for Python 3.9 :)
* Fix case of duplicate routes when cbv used with prefix. (As mentioned in [#36](https://github.com/yuval9313/FastApi-RESTful/pull/36))
* Made repeatable task pre activate (`wait_first`) to be float instead of boolean (Mentioned here [#45](https://github.com/yuval9313/FastApi-RESTful/pull/45)) 

## 0.2.4.1

* Another docs fix
* Rename package folder to small casing to ease imports

## 0.2.4

* Mostly docs fixes

## 0.2.2

* Add `Resorce` classes for more OOP like designing
* Methods are now can be used as class names

## 0.2.1

* Fix bug with multiple decorators on same method 

## 0.2.0

* Make some of the functions/classes in `fastapi_utils.timing` private to clarify the intended public API
* Add documentation for `fastapi_utils.timing` module 
* Fix bug with ordering of routes in a CBV router 

## 0.1.1

* Add source docstrings for most functions.

## 0.1.0

* Initial release.
