"""
Shared test configuration and utilities.
"""
import os
import tempfile

__all__ = ["fresh_duckdb_path"]


def fresh_duckdb_path() -> str:
    """
    Return a path to a brand-new DuckDB file.
    We create a temp name and *delete* the zero-byte file immediately,
    so DuckDB can initialise it itself.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)        # close handle
    os.unlink(path)     # remove file so DuckDB can create it
    return path