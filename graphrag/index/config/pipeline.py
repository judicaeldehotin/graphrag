# Copyright (c) 2024 Microsoft Corporation. All rights reserved.

"""A module containing 'PipelineConfig' model."""

from __future__ import annotations

from devtools import debug
from pydantic import BaseModel
from pydantic import Field as pydantic_Field

from .cache import PipelineCacheConfigTypes
from .input import PipelineInputConfigTypes
from .reporting import PipelineReportingConfigTypes
from .storage import PipelineStorageConfigTypes
from .workflow import PipelineWorkflowReference


class PipelineConfig(BaseModel):
    """Represent the configuration for a pipeline."""

    def __repr__(self):
        return str(debug.format(self))

    def __str__(self):
        return self.__repr__()

    extends: list[str] | str | None = pydantic_Field(
        description="Extends another pipeline configuration", default=None
    )
    """Extends another pipeline configuration"""
    input: PipelineInputConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """The input configuration for the pipeline."""
    reporting: PipelineReportingConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """The reporting configuration for the pipeline."""
    storage: PipelineStorageConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """The storage configuration for the pipeline."""
    cache: PipelineCacheConfigTypes | None = pydantic_Field(
        default=None, discriminator="type"
    )
    """The cache configuration for the pipeline."""
    root_dir: str | None = pydantic_Field(
        description="The root directory for the pipeline. All other paths will be based on this root_dir.",
        default=None,
    )
    """The root directory for the pipeline."""

    workflows: list[PipelineWorkflowReference] = pydantic_Field(
        description="The workflows for the pipeline.", default_factory=list
    )
    """The workflows for the pipeline."""
