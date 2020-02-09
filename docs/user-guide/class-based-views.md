#### Source module: [`fastapi_utils.cbv`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/cbv.py){.internal-link target=_blank}

---

As you create more complex FastAPI applications, you may find yourself
frequently repeating the same dependencies in multiple related endpoints.

A common question people have as they become more comfortable with FastAPI
is how they can reduce the number of times they have to copy/paste the same dependency
into related routes.

`fastapi_utils` provides a "class-based view" decorator (`@cbv`) to help reduce the amount of boilerplate
necessary when developing related routes.

## A basic CRUD app

Consider a basic create-read-update-delete (CRUD) app where users can create "Item" instances,
but only the user that created an item is allowed to view or modify it:

```python hl_lines="61 62 74 75 85 86 100 101"
{!./src/class_based_views1.py!}
```

If you look at the highlighted lines above, you can see `get_db`
and `get_jwt_user` repeated in each endpoint.


## The `@cbv` decorator

By using the `fastapi_utils.cbv.cbv` decorator, we can consolidate the
endpoint signatures and reduce the number of repeated dependencies.

To use the `@cbv` decorator, you need to:

1. Create an APIRouter to which you will add the endpoints
2. Create a class whose methods will be endpoints with shared depedencies, and decorate it with `@cbv(router)`
3. For each shared dependency, add a class attribute with a value of type `Depends`
4. Replace use of the original "unshared" dependencies with accesses like `self.dependency` 

Let's follow these steps to simplify the example above, while preserving all of the original logic:

```python hl_lines="11 58 61 63 64 65 69 70 71"
{!./src/class_based_views2.py!}
```

The highlighted lines above show the results of performing each of the numbered steps.

Note how the signature of each endpoint definition now includes only the parts specific
to that endpoint. 

(Also note that we've also used the [`InferringRouter`](inferring-router.md){.internal-link target=_blank}
here to remove the need to specify a `response_model` in the endpoint decorators.)

Hopefully this helps you to better reuse dependencies across endpoints!

!!! info
    While it is not demonstrated above, you can also make use of custom instance-initialization logic
    by defining an `__init__` method on the CBV class.
    
    Arguments to the `__init__` function are injected by FastAPI in the same way they would be for normal
    functions.
    
    You should **not** make use of any arguments to `__init__` with the same name as any annotated instance attributes
    on the class. Those values will be set as attributes on the class instance prior to calling the `__init__` function
    you define, so you can still safely access them inside your custom `__init__` function if desired.
     