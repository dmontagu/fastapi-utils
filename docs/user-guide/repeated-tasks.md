#### Source module: [`fastapi_utils.tasks`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/tasks.py){.internal-link target=_blank}

---

Startup and shutdown events are a great way to trigger actions related to the server lifecycle.

However, sometimes you want a task to trigger not just when the server starts, but also
on a periodic basis. For example, you might want to regularly reset an internal cache, or delete
expired tokens from a database.

You can accomplish this by triggering a loop inside a start-up event, but there are a few
challenges to overcome:

1. You finish the startup event before the periodic loop ends (so the server can start!)
2. If the repeated tasks performs blocking IO, it shouldn't block the event loop
3. Exceptions raised by the periodic task shouldn't just be silently swallowed

The `fastapi_utils.tasks.repeat_every` decorator handles all of these issues and adds some other conveniences as well.

## The `@repeat_every` decorator

When a function decorated with the `@repeat_every(...)` decorator is called, a loop is started,
and the function is called periodically with a delay determined by the `seconds` argument provided to the decorator.

If you *also* apply the `@app.event("startup")` decorator, FastAPI will call the function during server startup,
and the function will then be called repeatedly while the server is still running. 

Here's a hypothetical example that could be used to periodically clean up expired tokens:

```python hl_lines="5 18"
{!./src/repeated_tasks1.py!}
```

(You may want to reference the [sessions docs](session.md){.internal-link target=_blank} for more
information about `FastAPISessionMaker`.)

By passing `seconds=60 * 60`, we ensure that the decorated function is called once every hour.

Some other notes:

* The wrapped function should not take any required arguments.
* `repeat_every` function works right with both `async def` and `def` functions.
* `repeat_every` is safe to use with `def` functions that perform blocking IO -- they are executed in a threadpool
(just like `def` endpoints).


## Keyword arguments

Here is a more detailed description of the various keyword arguments for `repeat_every`:

* `seconds: float` : The number of seconds to wait between successive calls
* `wait_first: bool = False` : If `False` (the default), the wrapped function is called immediately when the decorated
function is first called. If `True`, the decorated function will wait one period before making the first call to the wrapped function
* `logger: Optional[logging.Logger] = None` : If you pass a logger, any exceptions raised in the repeating execution loop will be logged (with a traceback)
    to the provided logger.
* `raise_exceptions: bool = False`
    * If `False` (the default), exceptions are caught in the repeating execution loop, but are not raised. 
    If you leave this argument `False`, you'll probably want to provide a `logger` to ensure your repeated events
    don't just fail silently.
    * If `True`, an exception will be raised. 
    In order to handle this exception, you'll need to register an exception handler that is able to catch it
    For example, you could use `asyncio.get_running_loop().set_exception_handler(...)`, as documented 
    [here](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.set_exception_handler).
    * Note that if an exception is raised, the repeated execution will stop.   
* `max_repetitions: Optional[int] = None` : If `None` (the default), the decorated function will keep repeating forever.
Otherwise, it will stop repeated execution after the specified number of calls
