First, you might want to see the basic ways to [help and get help](help-fastapi-utils.md){.internal-link target=_blank}.

## Developing

Once you've cloned the repository, here are some guidelines to set up your environment:

### Set up the development evironment

After cloning the repository, you can use `poetry` to create a virtual environment: 

```console
$ make develop
```

Behind the scenes, this checks that you have python3 and poetry installed,
then creates a virtual environment and installs the dependencies. At the end, it will print out
the path to the executable in case you want to add it to your IDE.


### Activate the environment

Once the virtual environment is created, you can activate it with:

```console
$ poetry shell
```

To check if this worked, try running: 

```console
$ which python

some/directory/fastapi-utils-SOMETHING-py3.X/bin/python
```

If the output of this command shows the `python` binary in a path containing `fastapi-utils` somewhere in the name
(as above), then it worked! 🎉

!!! tip
    Every time you install a new package with `pip` under that environment, activate the environment again.

    This makes sure that if you use a terminal program installed by that package (like `mypy`),
    you use the one from your local environment and not any other that could be installed globally.

### Static Code Checks

This project makes use of `black`, `autoflake8`, and `isort` for formatting,
`flake8` for linting, and `mypy` for static type checking.


To auto-format your code, just run:

```console
$ make format
```

It will also auto-sort all your imports, and attempt to remove any unused imports.

You can run flake8 with:

```console
$ make lint
```

and you can run mypy with:

```console
$ make mypy
```

There are a number of other useful makefile recipes; you can see basic documentation of these by calling plain `make`:

```console
$ make
```


## Docs

The documentation uses <a href="https://www.mkdocs.org/" class="external-link" target="_blank">MkDocs</a>.

All the documentation is in Markdown format in the directory `./docs`.

Many of the sections in the User Guide have blocks of code.

In fact, those blocks of code are not written inside the Markdown, they are Python files in the `./docs/src/` directory.

And those Python files are included/injected in the documentation when generating the site.

### Docs for tests

Most of the tests actually run against the example source files in the documentation.

This helps making sure that:

* The documentation is up to date.
* The documentation examples can be run as is.
* Most of the features are covered by the documentation, ensured by test coverage.

During local development, there is a script that builds the site and checks for any changes, live-reloading:

```console
$ bash scripts/docs-live.sh
```

It will serve the documentation on `http://0.0.0.0:8008`.

That way, you can edit the documentation/source files and see the changes live.

## Tests

You can run all tests via:

```console
$ make test
```

You can also generate a coverage report with:

```console
make testcov
```

On MacOS, if the tests all pass, the coverage report will be opened directly in a browser; on other operating systems
a link will be printed to the local HTML containing the coverage report.

### Tests in your editor

If you want to use the integrated tests in your editor add `./docs/src` to your `PYTHONPATH` variable.

For example, in VS Code you can create a file `.env` with:

```env
PYTHONPATH=./docs/src
```
