"""Feature-block ablation utilities."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import pandas as pd


def leave_one_block_out_feature_sets(
    feature_blocks: Mapping[str, Sequence[str]],
) -> dict[str, list[str]]:
    """Return feature sets obtained by dropping one feature block at a time."""
    all_features = []
    for columns in feature_blocks.values():
        all_features.extend(columns)
    unique_features = list(dict.fromkeys(all_features))

    ablations: dict[str, list[str]] = {"full": unique_features}
    for block, columns in feature_blocks.items():
        dropped = set(columns)
        ablations[f"drop_{block}"] = [
            feature for feature in unique_features if feature not in dropped
        ]
    return ablations


def ablation_table(rows: Sequence[Mapping[str, object]]) -> pd.DataFrame:
    """Create a sorted ablation-result table from row dictionaries."""
    frame = pd.DataFrame(rows)
    if "ablation" in frame.columns:
        frame = frame.sort_values("ablation")
    return frame.reset_index(drop=True)
