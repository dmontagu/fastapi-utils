## Latest changes

## 0.3.0

* Move to ruff for linting, etc.
* Update various dependencies
* Stop supporting Python 3.6
* Deprecate InferringRouter (as its functionality is now built into `fastapi.APIRouter`)
* Resolve various deprecationwarnings introduced by sqlalchemy 1.4.
* Added support for Pydantic 2, you have to select the dependency in your project:
  - for v1 use `fastapi-utils = "^0.3"`, or `pydantic = "^1.10"`, or both,
  - for v2 use `fastapi-utils = { version = "^0.3", extras = ["pydantic_settings"] }`, or `pydantic = "^2.0"`, or both.

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
