"""
Shared test configuration and utilities.
"""
import os
import tempfile
import duckdb
from pathlib import Path


def fresh_duckdb_path() -> str:
    """
    Return a path to a brand-new DuckDB file.
    We create a temp name and *delete* the zero-byte file immediately,
    so DuckDB can initialise it itself.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    path = tmp.name
    tmp.close()
    os.unlink(path)          # <-- crucial line
    return path