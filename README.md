# Observatoire de la biodiversité de La Réunion

Ce dépôt explore une chaîne de données GBIF dans PostgreSQL et un agent Python capable de choisir des outils pour répondre à des questions sur ces données.

Sur la branche `feature/agent-tool-calling`, l’agent est un **prototype Gemini** : les outils renvoient des valeurs fixes. L’ingestion PostgreSQL existe séparément ; l’agent ne lui est pas encore connecté.

## Où trouver la documentation ?

- [Agent Python](docs/agent-python.md) : architecture, fichiers, installation, exécution et limites.
- [Données et PostgreSQL](docs/donnees-postgres.md) : imports GBIF, tables, contrôles SQL et prérequis.
- [Projet dbt](reunion_dbt/README.md) : état des transformations.

Le `README.md` sert de point d’entrée. Les guides détaillés sont dans `docs/`, avec des noms décrivant leur sujet. Les commentaires et docstrings expliquent les décisions au plus près du code. Lorsqu’un comportement change, mettre à jour le guide correspondant et ses commandes.

## Premier essai sans API ni base

Depuis la racine du dépôt, avec Python 3.12 :

```bash
python -m venv .venv-agent
source .venv-agent/bin/activate
python -m pip install google-genai pydantic python-dotenv
python agent/test_orchestrator.py
```

Le script affiche trois scénarios utilisant les outils simulés. Il vérifie également par assertions le nettoyage des arguments, le rejet des demandes invalides et la poursuite des appels après une erreur. Le dépôt ne fournit pas encore de manifeste Python ni de verrouillage des versions.

Les scripts Python sont exécutables directement et effectuent leurs opérations au niveau du module : importer un script d’ingestion ou un script Gemini peut déclencher un accès externe. Lire les prérequis avant de les lancer.
