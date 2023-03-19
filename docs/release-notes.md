## Latest changes

## 0.3.0

* Move to ruff for linting, etc.
* Update various dependencies
* Stop supporting Python 3.6
* Deprecate InferringRouter (as its functionality is now built into `fastapi.APIRouter`)
* Resolve various deprecationwarnings introduced by sqlalchemy 1.4.

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
