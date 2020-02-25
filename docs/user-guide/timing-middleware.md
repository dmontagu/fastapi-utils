#### Source module: [`fastapi_utils.timing`](https://github.com/dmontagu/fastapi-utils/blob/master/fastapi_utils/timing.py){.internal-link target=_blank}

---

The `fastapi_utils.timing` module provides basic profiling functionality that could be
used to find performance bottlenecks, monitor for regressions, etc.

There are currently two public functions provided by this module:

* `add_timing_middleware`, which can be used to add a middleware to a `FastAPI` app that will
log very basic profiling information for each request (with low overhead).

* `record_timing`, which can be called on a `starlette.requests.Request` instance for a `FastAPI`
app with the timing middleware installed (via `add_timing_middleware`), and will emit performance
information for the request at the point at which it is called.

!!! tip
    If you are look for more fine-grained performance profiling data, consider 
    <a href="https://github.com/sumerc/yappi" target="_blank">`yappi`</a>,
    a python profiling library that was recently updated with coroutine support to enable
    better coroutine-aware profiling.
    
    Note however that `yappi` adds considerable runtime overhead, and should typically be used during
    development rather than production.
    
    The middleware provided in this package is intended to be sufficiently performant for production use.
    

## Adding timing middleware

The `add_timing_middleware` function takes the following arguments:

* `app: FastAPI` : The app to which to add the timing middleware
* `record: Optional[Callable[[str], None]] = None` : The callable to call on the generated timing messages.
If not provided, defaults to `print`; a good choice is the `info` method of a `logging.Logger` instance 
* `prefix: str = ""` : A prefix to prepend to the generated route names. This can be useful for, e.g., 
distinguishing between mounted ASGI apps.
* `exclude: Optional[str] = None` : If provided, any route whose generated name includes this value will not have its
timing stats recorded.
 
Here's an example demonstrating what the logged output looks like (note that the commented output has been
split to multiple lines for ease of reading here, but each timing record is actually a single line): 

```python hl_lines="15 37 42 45 53"
{!./src/timing1.py!}
```

## Recording intermediate timings

In the above example, you can see the `get_with_intermediate_timing` function used in
the `/timed-intermediate` endpoint to record an intermediate execution duration:

```python hl_lines="33 46 47 48"
{!./src/timing1.py!}
```

Note that this requires the app that generated the `Request` instance to have had the timing middleware
added using the `add_timing_middleware` function.

This can be used to output multiple records at distinct times in order to introspect the relative
contributions of different execution steps in a single endpoint.