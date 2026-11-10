"""Affiche les observations annuelles du mart PostgreSQL."""

import pandas as pd
import psycopg
import streamlit as st
from analytics import annual_observations

st.set_page_config(
    page_title="Biodiversité de La Réunion",
    layout="wide",
)

st.title("Observations de biodiversité de La Réunion")


@st.cache_data(ttl=60)
def load_observations():
    """Lit le mart et garde les données en cache pendant 60 secondes."""
    with psycopg.connect(
        **dict(st.secrets["postgres"]),
        connect_timeout=10,
    ) as conn:
        # L’application lit les données sans modifier la base.
        conn.read_only = True

        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    observation_year,
                    genus,
                    observation_count
                FROM staging.mart_observations_annuelles
                ORDER BY observation_year, genus
            """)
            rows = cur.fetchall()

    # Transformer les résultats SQL en tableau pandas.
    return pd.DataFrame(
        rows,
        columns=[
            "observation_year",
            "genus",
            "observation_count",
        ],
    )


# Arrêter l’affichage si PostgreSQL est inaccessible.
try:
    observations = load_observations()
except psycopg.Error:
    st.error(
        "Impossible de lire le mart PostgreSQL. "
        "Vérifie la connexion et la présence de la table."
    )
    st.stop()

if observations.empty:
    st.info("Le mart ne contient aucune donnée.")
    st.stop()


# Proposer les genres renseignés ; None signifie « tous les genres ».
genres = sorted(
    observations["genus"].dropna().unique().tolist()
)

selected_genus = st.selectbox(
    "Genre",
    options=[None, *genres],
    format_func=lambda value: (
        "Tous les genres" if value is None else value
    ),
)

include_unknown = st.checkbox(
    "Inclure les observations sans genre",
    value=True,
    disabled=selected_genus is not None,
)


# Le filtrage et le calcul sont maintenant définis dans analytics.py.
annual = annual_observations(
    observations,
    selected_genus=selected_genus,
    include_unknown=include_unknown,
)

st.metric(
    "Observations sélectionnées",
    f"{int(annual.sum()):,}",
)

if annual.empty:
    st.info("Aucune observation pour cette sélection.")
else:
    st.bar_chart(
        annual.rename("Nombre d’observations"),
        x_label="Année d’observation",
        y_label="Nombre d’observations",
    )

st.caption(
    "Une observation représente un enregistrement GBIF, pas un individu. "
    "L’évolution des comptes dépend notamment de l’effort de collecte. "
    "Les données sont conservées en cache pendant 60 secondes."
)
