---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: bug
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

If you can generate a relevant traceback, please include it.

**To Reproduce**
Steps to reproduce the behavior:
1. Create a file with '...'
2. Add a path operation function with '....'
3. Open the browser and call it with a payload of '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Linux / Windows / macOS]
 - FastAPI Utils, FastAPI, and Pydantic versions [e.g. `0.3.0`], get them with:

```Python
import fastapi_utils
import fastapi
import pydantic.utils
print(fastapi_utils.__version__)
print(fastapi.__version__)
print(pydantic.utils.version_info())
```

- Python version, get it with:

```bash
python --version
```

**Additional context**
Add any other context about the problem here.
