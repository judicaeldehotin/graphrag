# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from graphrag.index.api import GraphRagIndexer


def test_initialize_project_at(tmp_path):
    """
    Directory Initialization
    equivalent to instruction: poetry run poe index --init --root ragtest
    """
    indexer = GraphRagIndexer(root="ragtest", init=True)
    indexer.run()


def test_initialize_index_at(tmp_path):
    """
    Index Initialization
    equivalent to instruction: poetry run poe index --root ragtest
    """
    indexer = GraphRagIndexer(root="ragtest")
    indexer.run()
