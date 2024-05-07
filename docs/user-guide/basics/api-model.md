#### Source module: [`fastapi_utils.api_model`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/api_model.py){.internal-link target=_blank}

---

One of the most common nuisances when developing a python web API is that python style typically involves
`snake_case` attributes, whereas typical JSON style is to use `camelCase` field names.

Fortunately, pydantic has built-in functionality to make it easy to have `snake_case` names for `BaseModel` attributes,
and use `snake_case` attribute names when initializing model instances in your own code,
but accept `camelCase` attributes from external requests.

Another `BaseModel` config setting commonly used with FastAPI is `orm_mode`, which allows your models
to be read directly from ORM objects (such as those used by SQLAlchemy). 

You can use `fastapi_utils.api_model.APIModel` to easily enable all of these frequently desirable settings.

## Create a model

To make use of `APIModel`, just use it instead of `pydantic.BaseModel` as the base class of your pydantic models:


```python hl_lines="7 12"
{!./src/api_model.py!}
```

!!! info
    You can use `typing.NewType` as above to (statically) ensure that you don't accidentally misuse an ID associated
    with one type of resource somewhere that an ID of another type of resource is expected.
    
    This is useful since it can be difficult, for example, to immediately recognize that you've passed a user ID where
    a product ID was supposed to go just by looking at its value. Using `typing.NewType` ensures mypy
    can check this for you. 

    For a more detailed explanation and example, see 
    [this GitHub issue comment](https://github.com/tiangolo/fastapi/issues/533#issuecomment-532597649)

Now, you can make requests to endpoints expecting `User` as the body using either snake case:

```JSON
{
  "user_id": "00000000-0000-0000-0000-000000000000",
  "email_address": "user@email.com"
}
``` 

or camel case:

```JSON
{
  "userId": "00000000-0000-0000-0000-000000000000",
  "emailAddress": "user@email.com"
}
```

and both will work.

In addition, if you set the `response_model` argument to the endpoint decorator and return an object that can't
be converted to a dict, but has appropriately named fields, FastAPI will use pydantic's `orm_mode` to automatically
serialize it.

```python hl_lines="30 32"
{!./src/api_model.py!}
```
