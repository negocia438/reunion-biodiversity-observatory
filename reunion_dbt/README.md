# Transformations dbt de l’observatoire

Ce répertoire prépare les transformations des données GBIF. Il déclare actuellement la source `raw.gbif_occurrences_full` dans `models/staging/gbif/_gbif__sources.yml`, sans modèle SQL de transformation ni test de données.

`dbt_project.yml` utilise encore le nom de profil `jaffle_shop`, hérité du projet initial. Pour utiliser dbt, installer un moteur et un adaptateur PostgreSQL compatibles, puis configurer ce profil dans `~/.dbt/profiles.yml` avec les paramètres de votre instance. Conserver les identifiants hors du dépôt et utiliser des variables d’environnement pour les secrets.

Depuis ce répertoire, avec dbt configuré :

```bash
dbt deps
dbt debug
dbt parse
```

`dbt debug` vérifie notamment la connexion ; `dbt parse` vérifie la lecture du projet. Un `dbt build` sans modèle ni test ne valide aucune transformation métier. Cette configuration dbt et sa connexion ne sont pas encore vérifiées dans l’environnement cloud.

Consulter le [guide des données](../docs/donnees-postgres.md) pour les imports et le [guide de l’agent](../docs/agent-python.md) pour le prototype Python.
