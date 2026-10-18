import os
import zipfile
import xml.etree.ElementTree as ET

import psycopg
from psycopg import sql


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ZIP_PATH = "data/gbif/raw/0021471-260928105237408.zip"

DB_HOST = "localhost"
DB_NAME = "reunion_biodiversity"
DB_USER = "reunion_user"

SCHEMA_NAME = "raw"
TABLE_NAME = "gbif_occurrences_full"

NAMESPACE = {
    "dwc": "http://rs.tdwg.org/dwc/text/"
}


# --------------------------------------------------
# 1. Lire meta.xml et récupérer les colonnes GBIF
# --------------------------------------------------

columns = []

with zipfile.ZipFile(ZIP_PATH) as archive:
    with archive.open("meta.xml") as meta_file:

        tree = ET.parse(meta_file)
        root = tree.getroot()

        core = root.find("dwc:core", NAMESPACE)

        if core is None:
            raise ValueError(
                "Impossible de trouver <core> dans meta.xml."
            )

        fields = core.findall("dwc:field", NAMESPACE)

        for field in fields:

            index = field.get("index")
            term = field.get("term")

            # Certains <field> peuvent ne pas avoir d'index
            if index is None or term is None:
                continue

            # Exemple :
            # http://rs.tdwg.org/dwc/terms/scientificName
            # devient :
            # scientificName
            column_name = term.rsplit("/", 1)[-1]

            columns.append(
                (int(index), column_name)
            )


# Respecter l'ordre physique des colonnes dans occurrence.txt
columns.sort(key=lambda column: column[0])

print(f"{len(columns)} colonnes GBIF détectées.")


# --------------------------------------------------
# 2. Construire les définitions SQL
# --------------------------------------------------

sql_columns = []

for _, column_name in columns:

    column_definition = sql.SQL("{} TEXT").format(
        sql.Identifier(column_name)
    )

    sql_columns.append(column_definition)


# --------------------------------------------------
# 3. Construire le CREATE TABLE
# --------------------------------------------------

create_table_query = sql.SQL(
    """
    CREATE TABLE IF NOT EXISTS {}.{} (
        {}
    )
    """
).format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME),
    sql.SQL(", ").join(sql_columns)
)


# --------------------------------------------------
# 4. Connexion PostgreSQL
# --------------------------------------------------

password = os.environ["DB_PASSWORD"]

conn = psycopg.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=password
)


# --------------------------------------------------
# 5. Créer la table RAW
# --------------------------------------------------

with conn:
    with conn.cursor() as cur:

        cur.execute(create_table_query)


print(
    f"Table {SCHEMA_NAME}.{TABLE_NAME} créée "
    f"avec {len(columns)} colonnes."
)