from importlib import metadata

__version__ = "0.2.0"

# Warn #2 guard: if __version__ were ever deleted or set to None,
# this assert will fail fast at import time instead of silently breaking
# pip install (which reads this attribute via setuptools dynamic versioning).
assert isinstance(__version__, str) and __version__, (
    "hyperflow/__version__ must be a non-empty string "
    "(required by pyproject.toml dynamic versioning)"
)


def get_version() -> str:
    try:
        return metadata.version("hyperflow")
    except metadata.PackageNotFoundError:
        return __version__
