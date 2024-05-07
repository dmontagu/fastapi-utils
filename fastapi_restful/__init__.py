import sys
import warnings

from .cbv_base import Api, Resource, set_responses, take_init_parameters

if sys.version_info.minor < 8:
    import pkg_resources

    try:
        __version__ = pkg_resources.get_distribution(__name__).version
    except pkg_resources.DistributionNotFound as e:
        warnings.warn(f"Could not determine version of {__name__}", stacklevel=1)
        warnings.warn(str(e), stacklevel=1)
        __version__ = "unknown"
else:
    import importlib.metadata

    try:
        __version__ = importlib.metadata.version(__name__)
    except importlib.metadata.PackageNotFoundError as e:
        warnings.warn(f"Could not determine version of {__name__}", stacklevel=1)
        warnings.warn(str(e), stacklevel=1)
        __version__ = "unknown"


__all__ = [
    "Api",
    "Resource",
    "set_responses",
    "take_init_parameters",
]
