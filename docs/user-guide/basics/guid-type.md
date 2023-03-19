#### Source module: [`fastapi_utils.guid_type`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/guid_type.py){.internal-link target=_blank}

---

The two most common types used for primary keys in database tables are integers and UUIDs
(sometimes referred to as GUIDs).

There are a number of tradeoffs to make when deciding whether to use integers vs. UUIDs,
including:

* UUIDs don't reveal anything about the number of records in a table
* UUIDs are practically impossible for an adversary to guess (though you shouldn't rely solely on that for security!)
* UUIDs are harder to communicate/remember
* UUIDs may result in worse performance for certain access patterns due to the random ordering

You'll have to decide based on your application which is right for you, but if you want to
use UUIDs/GUIDs for your primary keys, there are some difficulties to navigate.

## Challenges using UUID-valued primary keys with sqlalchemy
 
Python has support for UUIDs in the standard library, and most relational databases
have good support for them as well.

However, if you want a database-agnostic or database-driver-agnostic type, you may run into
challenges.

In particular, the postgres-compatible UUID type provided by sqlalchemy (`sqlalchemy.dialects.postgresql.UUID`)
will not work with other databases, and it also doesn't come with a way to set a server-default, meaning that
you'll always need to take responsibility for generating an ID in your application code.

Even worse, if you try to use the postgres-compatible UUID type simultaneously with both `sqlalchemy` and the
`encode/databases` package, you may run into issues where queries using one require you to set `UUID(as_uuid=True)`,
when declaring the column, and the other requires you to declare the table using `UUID(as_uuid=False)`.

Fortunately, sqlalchemy provides a 
[backend-agnostic implementation of GUID type](https://docs.sqlalchemy.org/en/13/core/custom_types.html#backend-agnostic-guid-type)
that uses the postgres-specific UUID type when possible, and more carefully parses the result to ensure
`uuid.UUID` isn't called on something that is already a `uuid.UUID` (which raises an error).

For convenience, this package includes this `GUID` type, along with conveniences for setting up server defaults
for primary keys of this type.

## Using GUID

You can create a sqlalchemy table with a GUID as a primary key using the declarative API like this:

```python hl_lines=""
{!./src/guid1.py!}
```

## Server Default
If you want to add a server default, it will no longer be backend-agnostic, but
you can use `fastapi_utils.guid_type.GUID_SERVER_DEFAULT_POSTGRESQL`: 

```python
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from fastapi_utils.guid_type import GUID, GUID_SERVER_DEFAULT_POSTGRESQL

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(
        GUID,
        primary_key=True,
        server_default=GUID_SERVER_DEFAULT_POSTGRESQL
    )
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)
```
(Behind the scenes, this is essentially just setting the server-side default to `"gen_random_uuid()"`.)

Note this will only work if you have installed the `pgcrypto` extension
in your postgres instance. If the user you connect with has the right privileges, this can be done
by calling the `fastapi_utils.guid_type.setup_guids_postgresql` function:

```python
{!./src/guid2.py!}
```

## Non-Server Default

If you are comfortable having no server default for your primary key column, you can still
make use of an application-side default (so that `sqlalchemy` will generate a default value when you
create new records):

```python
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = sa.Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = sa.Column(sa.String, nullable=False)
    related_id = sa.Column(GUID)
```

`GUID_DEFAULT_SQLITE` is just an alias for the standard library `uuid.uuid4`,
which could be used in its place. 
