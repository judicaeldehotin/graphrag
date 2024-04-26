# Copyright (c) 2024 Microsoft Corporation. All rights reserved.
"""Indexing-Engine to Query Read Adapters.

The parts of these functions that do type adaptation, renaming, collating, etc. should eventually go away.
Ideally this is just a straight read-thorugh into the object model.
"""

from typing import cast

import pandas as pd

from graphrag.model import CommunityReport, Covariate, Entity, Relationship, TextUnit
from graphrag.query.input.loaders.dfs import (
    read_community_reports,
    read_covariates,
    read_entities,
    read_relationships,
    read_text_units,
)
from graphrag.query.input.retrieval.relationships import (
    calculate_relationship_combined_rank,
)


def read_indexer_text_units(final_text_units: pd.DataFrame) -> list[TextUnit]:
    """Read in the Text Units from the raw indexing outputs."""
    return read_text_units(
        df=final_text_units,
        short_id_col=None,
        # expects a covariate map of type -> ids
        covariates_col=None,
    )


def read_indexer_covariates(final_covariates: pd.DataFrame) -> list[Covariate]:
    """Read in the Claims from the raw indexing outputs."""
    covariate_df = final_covariates
    covariate_df["id"] = covariate_df["id"].astype(str)
    return read_covariates(
        df=covariate_df,
        short_id_col=None,
        attributes_cols=[
            "object_id",
            "status",
            "start_date",
            "end_date",
            "description",
        ],
        text_unit_ids_col=None,
    )


def read_indexer_relationships(
    final_relationships: pd.DataFrame, entities: list[Entity]
) -> list[Relationship]:
    """Read in the Relationships from the raw indexing outputs."""
    relationship_df = final_relationships
    relationship_df["id"] = relationship_df["id"].astype(str)
    relationship_df["human_readable_id"] = relationship_df["human_readable_id"].astype(
        str
    )
    relationship_df["weight"] = relationship_df["weight"].astype(float)
    relationship_df["text_unit_ids"] = relationship_df["text_unit_ids"].apply(
        lambda x: x.split(",")
    )
    relationship_df = cast(
        pd.DataFrame,
        relationship_df[
            [
                "id",
                "human_readable_id",
                "source",
                "target",
                "description",
                "weight",
                "text_unit_ids",
            ]
        ],
    )
    relationships = read_relationships(
        df=relationship_df,
        id_col="id",
        short_id_col="human_readable_id",
        source_col="source",
        target_col="target",
        description_col="description",
        weight_col="weight",
        description_embedding_col=None,
        text_unit_ids_col="text_unit_ids",
        document_ids_col=None,
    )
    return calculate_relationship_combined_rank(
        relationships=relationships, entities=entities, ranking_attribute="rank"
    )


def read_indexer_reports(
    final_community_reports: pd.DataFrame,
    final_nodes: pd.DataFrame,
    community_level: int,
) -> list[CommunityReport]:
    """Read in the Community Reports from the raw indexing outputs."""
    report_df = final_community_reports
    entity_df = final_nodes
    entity_df = cast(
        pd.DataFrame,
        entity_df[
            (entity_df.type == "entity")
            & (entity_df.level <= f"level_{community_level}")
        ],
    )
    entity_df["community"] = entity_df["community"].fillna(-1)
    entity_df["community"] = entity_df["community"].astype(int)

    entity_df = entity_df.groupby(["title"]).agg({"community": "max"}).reset_index()
    entity_df["community"] = entity_df["community"].astype(str)
    filtered_community_df = entity_df.rename(columns={"community": "community_id"})[
        "community_id"
    ].drop_duplicates()

    report_df = cast(
        pd.DataFrame, report_df[report_df.level <= f"level_{community_level}"]
    )

    report_df["rank"] = report_df["rank"].fillna(-1)
    report_df["rank"] = report_df["rank"].astype(int)

    report_df = report_df.merge(filtered_community_df, on="community_id", how="inner")

    return read_community_reports(
        df=report_df,
        id_col="community_id",
        short_id_col="community_id",
        community_col="community_id",
        title_col="title",
        summary_col="summary",
        content_col="full_content",
        rank_col="rank",
        summary_embedding_col=None,
        content_embedding_col=None,
    )


def read_indexer_entities(
    final_nodes: pd.DataFrame,
    final_entities: pd.DataFrame,
    community_level: int,
) -> list[Entity]:
    """Read in the Entities from the raw indexing outputs."""
    entity_df = final_nodes
    entity_embedding_df = final_entities

    entity_df = cast(
        pd.DataFrame,
        entity_df[
            (entity_df.type == "entity")
            & (entity_df.level <= f"level_{community_level}")
        ],
    )
    entity_df = cast(pd.DataFrame, entity_df[["title", "degree", "community"]]).rename(
        columns={"title": "name", "degree": "rank"}
    )

    entity_df["community"] = entity_df["community"].fillna(-1)
    entity_df["community"] = entity_df["community"].astype(int)
    entity_df["rank"] = entity_df["rank"].astype(int)

    # for duplicate entities, keep the one with the highest community level
    entity_df = (
        entity_df.groupby(["name", "rank"]).agg({"community": "max"}).reset_index()
    )
    entity_df["community"] = entity_df["community"].apply(lambda x: [str(x)])

    entity_embedding_df = entity_embedding_df[
        [
            "id",
            "human_readable_id",
            "name",
            "type",
            "description",
            "description_embedding",
            "text_unit_ids",
        ]
    ]

    entity_df = entity_df.merge(
        entity_embedding_df, on="name", how="inner"
    ).drop_duplicates(subset=["name"])

    # read entity dataframe to knowledge model objects
    return read_entities(
        df=entity_df,
        id_col="id",
        title_col="name",
        type_col="type",
        short_id_col="human_readable_id",
        description_col="description",
        community_col="community",
        rank_col="rank",
        name_embedding_col=None,
        description_embedding_col="description_embedding",
        graph_embedding_col=None,
        text_unit_ids_col="text_unit_ids",
        document_ids_col=None,
    )


def _filter_under_community_level_str(
    df: pd.DataFrame, community_level: int
) -> pd.DataFrame:
    return cast(
        pd.DataFrame,
        df[df.level <= f"level_{community_level}"],
    )


def _entity_communities_under_level(
    nodes: pd.DataFrame, community_level: int
) -> pd.Series:
    entity_df = _filter_under_community_level_str(nodes, community_level)
    entity_df["community"] = entity_df["community"].fillna(-1)
    entity_df["community"] = entity_df["community"].astype(int)
    entity_df = entity_df.groupby(["title"]).agg({"community": "max"}).reset_index()
    entity_df["community"] = entity_df["community"].astype(str)
    return cast(pd.Series, entity_df["community"].drop_duplicates())