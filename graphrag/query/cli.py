# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Command line interface for the query module."""

import re
from pathlib import Path

from graphrag.index.progress import PrintProgressReporter

from . import api

reporter = PrintProgressReporter("")


def run_global_search(
    config_dir: str | None,
    data_dir: str | None,
    root_dir: str | None,
    community_level: int,
    response_type: str,
    query: str,
):
    """Perform a global search with a given query.

    Loads index files required for global search and calls the Query API.
    """
    search_runner = api.SearchRunner(
        config_dir=config_dir,
        data_dir=data_dir,
        root_dir=root_dir,
        community_level=community_level,
        response_type=response_type,
    )
    return search_runner.run_global_search(query=query)


def run_local_search(
    config_dir: str | None,
    data_dir: str | None,
    root_dir: str | None,
    community_level: int,
    response_type: str,
    query: str,
):
    """Perform a local search with a given query.

    Loads index files required for local search and calls the Query API.
    """
    search_runner = api.SearchRunner(
        config_dir=config_dir,
        data_dir=data_dir,
        root_dir=root_dir,
        community_level=community_level,
        response_type=response_type,
    )
    return search_runner.run_local_search(query=query)


def _infer_data_dir(root: str) -> str:
    output = Path(root) / "output"
    # use the latest data-run folder
    if output.exists():
        expr = re.compile(r"\d{8}-\d{6}")
        filtered = [f for f in output.iterdir() if f.is_dir() and expr.match(f.name)]
        folders = sorted(filtered, key=lambda f: f.name, reverse=True)
        if len(folders) > 0:
            folder = folders[0]
            return str((folder / "artifacts").absolute())
    msg = f"Could not infer data directory from root={root}"
    raise ValueError(msg)
