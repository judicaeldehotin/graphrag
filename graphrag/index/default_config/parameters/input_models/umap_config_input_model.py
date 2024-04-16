# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""Parameterization settings for the default configuration."""

from typing import TypedDict

from typing_extensions import NotRequired


class UmapConfigInputModel(TypedDict):
    """Configuration section for UMAP."""

    enabled: NotRequired[bool | str | None]
