def annual_observations(
    observations,
    selected_genus=None,
    include_unknown=True,
):
    """Filtre le mart puis additionne les compteurs par année."""
    filtered = observations.copy()

    if selected_genus is not None:
        filtered = filtered[filtered["genus"] == selected_genus]
    elif not include_unknown:
        filtered = filtered[filtered["genus"].notna()]

    return (
        filtered.groupby("observation_year")["observation_count"]
        .sum()
        .sort_index()
    )
