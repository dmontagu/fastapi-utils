#### Source module: [`fastapi_utils.enums`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/enums.py){.internal-link target=_blank}

---

Using enums as fields of a JSON payloads is a great way to force provided values into one
of a limited number of self-documenting fields.

However, integer-valued enums can make it more difficult to inspect payloads and debug endpoint calls,
especially if the client and server are using different code bases.

For most applications, the development benefits of using string-valued enums vastly outweigh the
minimal performance/bandwidth tradeoffs.

Creating a string-valued enum for use with pydantic/FastAPI that is properly encoded in the OpenAPI spec is
as easy as inheriting from `str` in addition to `enum.Enum`:

```python
from enum import Enum

class MyEnum(str, Enum):
    value_a = "value_a"
    value_b = "value_b"
``` 

One nuisance with this approach is that if you rename one of the enum values (for example, using an IDE),
you can end up with the name and value differing, which may lead to confusing errors.

For example, if you refactored the above as follows (forgetting to çhange the associated values), you'll get
pydantic parsing errors if you use the new *names* instead of the values in JSON bodies:  

```python
from enum import Enum

class MyEnum(str, Enum):
    choice_a = "value_a"  # pydantic would only parse "value_a" to MyEnum.choice_a
    choice_b = "value_b"
``` 

The standard library's `enum` package provides a way to automatically generate values: 
[`auto`](https://docs.python.org/3/library/enum.html#enum.auto).

By default, `auto` will generate integer values, but this behavior can be overridden
and the official python docs include a detailed section about
[how to do this](https://docs.python.org/3/library/enum.html#using-automatic-values).

Rather than repeating this definition in each new project, to reduce boilerplate
you can just inherit from `fastapi_utils.enums.StrEnum` directly to get this behavior:

```python hl_lines="3 6"
{!./src/enums1.py!}
```

You can also use `fastapi_utils.enums.CamelStrEnum` to get camelCase values:

```python hl_lines="3 6"
{!./src/enums2.py!}
```
