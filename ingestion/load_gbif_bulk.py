import os
import zipfile
import csv
import io

import psycopg
from psycopg import sql


# --------------------------------------------------
# Configuration
# --------------------------------------------------

ZIP_PATH = "data/gbif/raw/0021471-260928105237408.zip"
OCCURRENCE_FILE = "occurrence.txt"

DB_HOST = "localhost"
DB_NAME = "reunion_biodiversity"
DB_USER = "reunion_user"

SCHEMA_NAME = "raw"
TABLE_NAME = "gbif_occurrences_full"


# --------------------------------------------------
# 1. Récupération du mot de passe PostgreSQL
# --------------------------------------------------

password = os.environ["DB_PASSWORD"]


# --------------------------------------------------
# 2. Connexion PostgreSQL
# --------------------------------------------------

conn = psycopg.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=password
)


# --------------------------------------------------
# 3. Construction de la commande COPY
# --------------------------------------------------

copy_query = sql.SQL("""
    COPY {}.{}
    FROM STDIN
""").format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME)
)


# --------------------------------------------------
# 4. Ouverture du ZIP et lecture du fichier GBIF
# --------------------------------------------------

print("Début du chargement GBIF...")

with zipfile.ZipFile(ZIP_PATH) as archive:

    with archive.open(OCCURRENCE_FILE) as occurrence_file:

        # Conversion des octets en texte UTF-8
        text_file = io.TextIOWrapper(
            occurrence_file,
            encoding="utf-8",
            newline=""
        )

        # Parsing du TSV GBIF
        reader = csv.reader(
            text_file,
            delimiter="\t",
            quoting=csv.QUOTE_NONE
        )

        # Première ligne = noms des colonnes
        header = next(reader)

        expected_columns = len(header)
        row_count = 0

        print(
            f"{expected_columns} colonnes détectées."
        )


        # --------------------------------------------------
        # 5. Chargement PostgreSQL avec COPY
        # --------------------------------------------------

        with conn:

            with conn.cursor() as cur:

                with cur.copy(copy_query) as copy:

                    for row in reader:

                        row_count += 1

                        # Sécurité : vérification du nombre de colonnes
                        if len(row) != expected_columns:
                            raise ValueError(
                                f"Ligne {row_count + 1} : "
                                f"{len(row)} colonnes au lieu de "
                                f"{expected_columns}"
                            )

                        # Envoi d'une observation structurée
                        # vers PostgreSQL
                        copy.write_row(row)

                        # Affichage de progression
                        if row_count % 100000 == 0:
                            print(
                                f"{row_count} observations chargées..."
                            )


# --------------------------------------------------
# 6. Fermeture
# --------------------------------------------------

conn.close()

print(
    f"Chargement terminé : "
    f"{row_count} observations chargées."
)