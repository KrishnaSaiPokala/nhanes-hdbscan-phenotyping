from nhanes_hdbscan.results import parse_ablation_key


def test_parse_ablation_key():
    assert parse_ablation_key("('noise_rate', 'mean')") == ("noise_rate", "mean")
    assert parse_ablation_key("('ARI_vs_full_reference', 'std')") == (
        "ARI_vs_full_reference",
        "std",
    )
