## Latest changes

## 0.5.0

* Move to ruff for linting, etc.
* Update various dependencies
* Stop supporting Python 3.6
* Deprecate InferringRouter (as its functionality is now built into `fastapi.APIRouter`)
* Resolve various deprecationwarnings introduced by sqlalchemy 1.4.

## 0.3.1

* [CVE-2021-29510](https://github.com/samuelcolvin/pydantic/security/advisories/GHSA-5jqp-qgf6-3pvh) fix of pydantic - update is required
* Made sqlalchemy as extras installs 

## 0.3.0

* Add support for Python 3.9 :)
* Fix case of duplicate routes when cbv used with prefix. (As mentioned in [#36](https://github.com/yuval9313/FastApi-RESTful/pull/36))
* Made repeatable task pre activate (`wait_first`) to be float instead of boolean (Mentioned here [#45](https://github.com/yuval9313/FastApi-RESTful/pull/45)) 

## 0.2.4.1

* Another docs fixes
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
