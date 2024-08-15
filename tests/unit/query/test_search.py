# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from ragtest.graphrag_test import SearchRunner


def test_local_search(query):
    """
    test local search
    equivalent to instruction: poetry run poe query --method local --root ragtest "question"
    """
    searcher = SearchRunner(root_dir="ragtest")
    searcher.run_local_search(query=query)


def test_global_search(query):
    """
    test global search
    equivalent to instruction: poetry run poe query --method local --root ragtest "question"
    """
    searcher = SearchRunner(root_dir="ragtest")
    searcher.run_global_search(query=query)


def test_remove_sources():
    """
    Delete special characters such a: [Data: Sources (82, 14, 42, 98)]
    """
    searcher = SearchRunner(root_dir="ragtest")
    searcher.remove_sources(searcher.run_local_search(query=""))
