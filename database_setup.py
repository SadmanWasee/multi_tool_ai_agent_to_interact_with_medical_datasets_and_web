
import csv
import sqlite3
from pathlib import Path

# Project directories
DATA_DIR = Path("data")
DB_DIR = Path("databases")
DB_DIR.mkdir(exist_ok=True)

# Dataset configurations
DATASETS = {
    "heart": {
        "csv_file": "heart.csv",
        "db_file": "heart_disease.db",
        "table": "heart_disease_records",
        "schema": {
            "age": "INTEGER",
            "sex": "INTEGER",
            "cp": "INTEGER",
            "trestbps": "INTEGER",
            "chol": "INTEGER",
            "fbs": "INTEGER",
            "restecg": "INTEGER",
            "thalach": "INTEGER",
            "exang": "INTEGER",
            "oldpeak": "REAL",
            "slope": "INTEGER",
            "ca": "INTEGER",
            "thal": "INTEGER",
            "target": "INTEGER"
        }
    },
    "cancer": {
        "csv_file": "The_Cancer_data_1500_V2.csv",
        "db_file": "cancer.db",
        "table": "cancer_records",
        "schema": {
            "Age": "INTEGER",
            "Gender": "INTEGER",
            "BMI": "REAL",
            "Smoking": "INTEGER",
            "GeneticRisk": "INTEGER",
            "PhysicalActivity": "REAL",
            "AlcoholIntake": "REAL",
            "CancerHistory": "INTEGER",
            "Diagnosis": "INTEGER"
        }
    }
}


def convert_value(value, data_type):
    """Convert CSV values into appropriate Python types."""
    if value is None or value.strip() == "":
        return None

    if data_type == "INTEGER":
        return int(value)

    if data_type == "REAL":
        return float(value)

    return value


def create_database(config):
    csv_path = DATA_DIR / config["csv_file"]
    db_path = DB_DIR / config["db_file"]
    table_name = config["table"]
    schema = config["schema"]

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    # Read and validate CSV
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != list(schema.keys()):
            raise ValueError(
                f"Unexpected columns in {csv_path.name}.\n"
                f"Expected: {list(schema.keys())}\n"
                f"Found: {reader.fieldnames}"
            )

        rows = list(reader)

    # Create SQL table definition
    columns = ", ".join(
        f'"{column}" {data_type}'
        for column, data_type in schema.items()
    )

    placeholders = ", ".join(["?"] * len(schema))
    column_names = ", ".join(f'"{column}"' for column in schema)

    # Convert CSV records
    records = [
        tuple(
            convert_value(row[column], schema[column])
            for column in schema
        )
        for row in rows
    ]

    # Create and populate SQLite database
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        )

        # Clear previous records to avoid duplicates on reruns
        connection.execute(f"DELETE FROM {table_name}")

        connection.executemany(
            f"INSERT INTO {table_name} ({column_names}) "
            f"VALUES ({placeholders})",
            records
        )

        inserted_count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]

    print(f"\nDatabase created: {db_path}")
    print(f"Table: {table_name}")
    print(f"Records inserted: {inserted_count}")


def main():
    for name, config in DATASETS.items():
        print(f"\nCreating {name} database...")
        create_database(config)

    print("\nAll databases created successfully!")


if __name__ == "__main__":
    main()
