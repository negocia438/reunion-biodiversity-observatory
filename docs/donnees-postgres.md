# Données GBIF et PostgreSQL

## Deux parcours d’import

| Parcours | Script | Table cible |
| --- | --- | --- |
| API : dix résultats pour `country=RE` | `ingestion/load_gbif.py` | `raw.gbif_occurrences` |
| Archive Darwin Core | `ingestion/generate_gbif_raw_schema.py`, puis `ingestion/load_gbif_bulk.py` | `raw.gbif_occurrences_full` |

La première table sélectionne des champs en snake_case et conserve des données JSON. La seconde conserve les noms des champs GBIF et utilise exclusivement des colonnes `TEXT`. Elles ne sont pas interchangeables. L’agent Python n’interroge encore aucune de ces tables.

## Prérequis

Les scripts utilisent actuellement `localhost`, la base `reunion_biodiversity` et le rôle `reunion_user`, codés en dur. Définir `DB_HOST` dans l’environnement ne modifie pas leur connexion. Le mot de passe est lu dans `DB_PASSWORD` ; les scripts d’ingestion ne chargent pas `.env` eux-mêmes.

La base, le rôle avec ses permissions et le schéma `raw` doivent déjà exister. Dans le cloud, `localhost` désigne la machine cloud, pas votre PC. Conserver les mots de passe dans une configuration sécurisée, hors du dépôt.

Depuis la racine :

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install requests 'psycopg[binary]'
```

## Import API

```bash
python ingestion/load_gbif.py
```

Le script appelle `https://api.gbif.org/v1/occurrence/search`, vérifie le statut HTTP puis insère les observations dans une transaction. Il ne pagine pas et ne définit pas de délai maximal HTTP.

La définition SQL de `raw.gbif_occurrences` est absente du dépôt. Elle doit correspondre aux colonnes insérées, avec une contrainte unique sur `gbif_key` pour `ON CONFLICT`. Les contrôles qualité nécessitent des dates et coordonnées comparables, et `issues` au format tableau JSONB. Ne pas confondre cette table avec celle générée depuis l’archive.

## Import d’archive

Placer le ZIP attendu à cet emplacement ignoré par Git :

```text
data/gbif/raw/0021471-260928105237408.zip
```

Il doit contenir `meta.xml` et `occurrence.txt` à sa racine. Vérifier sa provenance et sa somme SHA-256 ; les métadonnées de référence figurent dans `sql/schema/register_initial_gbif_source.sql`.

```bash
python ingestion/generate_gbif_raw_schema.py
python ingestion/load_gbif_bulk.py
```

Le générateur trie les éléments `field` de `meta.xml` par index. Il ne traite pas séparément l’élément Darwin Core `id` : vérifier la correspondance exacte entre les colonnes générées et le TSV. `CREATE TABLE IF NOT EXISTS` ne met pas à jour une table existante.

Le chargeur saute l’en-tête, vérifie la largeur des lignes et utilise `COPY` dans une transaction. L’ordre de la table doit correspondre au TSV. Une erreur annule la transaction ; un nouvel import réussi peut créer des doublons. Les chaînes vides sont transmises comme telles.

## Registre des fichiers sources

Depuis la racine, avec PostgreSQL configuré :

```bash
psql -h localhost -U reunion_user -d reunion_biodiversity -v ON_ERROR_STOP=1 -f sql/schema/create_source_files.sql
psql -h localhost -U reunion_user -d reunion_biodiversity -v ON_ERROR_STOP=1 -f sql/schema/register_initial_gbif_source.sql
```

Le premier crée `raw.source_files` ; le second enregistre les métadonnées de l’archive initiale. Ils ne sont pas idempotents : une seconde exécution peut échouer sur la table existante ou les contraintes uniques. L’ingestion ne met pas automatiquement ce registre à jour. `psql` ne lit pas automatiquement la variable Python `DB_PASSWORD` et peut demander le mot de passe.

## Contrôles qualité

Pour exécuter un contrôle, remplacer le nom du fichier selon le tableau :

```bash
psql -h localhost -U reunion_user -d reunion_biodiversity -v ON_ERROR_STOP=1 -f sql/quality/check_required_fields.sql
```

| Fichier dans `sql/quality/` | Mesure et limite |
| --- | --- |
| `check_required_fields.sql` | Au moins un champ obligatoire NULL ; ne détecte pas les chaînes vides. |
| `check_future_dates.sql` | Date postérieure à l’heure PostgreSQL. |
| `check_geographic_bounds.sql` | Hors latitude `[-21.40, -20.80]` ou longitude `[55.20, 55.90]` ; rectangle approximatif et NULL exclus. |
| `gbif_issue_distribution.sql` | Déplie le tableau JSONB `issues` et compte chaque problème. |

Ces requêtes ciblent `raw.gbif_occurrences`. Elles lisent les données et produisent des indicateurs, sans corriger les lignes ni échouer automatiquement si un compteur est non nul.

## Transformations

Le projet [dbt](../reunion_dbt/README.md) déclare la source `raw.gbif_occurrences_full`, sans modèle SQL de transformation. Son profil porte encore le nom `jaffle_shop` et nécessite une configuration externe. Une future couche métier pourra servir d’interface stable à l’agent.
