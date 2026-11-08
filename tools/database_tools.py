
import sqlite3
from pathlib import Path

from langchain_core.tools import tool


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "databases"


def execute_query(db_filename, query, params=()):
    """Execute a read-only SQL query and return its results."""

    db_path = DB_DIR / db_filename

    connection = sqlite3.connect(
        f"file:{db_path.as_posix()}?mode=ro",
        uri=True
    )

    try:
        connection.execute("PRAGMA query_only = ON")
        cursor = connection.execute(query, params)
        return cursor.fetchall()
    finally:
        connection.close()


@tool("HeartDiseaseDBTool")
def heart_disease_db_tool(question: str) -> str:
    """Retrieve statistics and information from the Heart Disease dataset."""

    question = question.lower()

    try:
        if any(word in question for word in ["count", "number", "how many", "records"]):
            result = execute_query(
                "heart_disease.db",
                "SELECT COUNT(*) FROM heart_disease_records"
            )
            return f"The Heart Disease dataset contains {result[0][0]} records."

        if "average age" in question or "mean age" in question:
            result = execute_query(
                "heart_disease.db",
                "SELECT AVG(age) FROM heart_disease_records"
            )
            return f"The average age is {result[0][0]:.2f} years."

        if "average cholesterol" in question or "mean cholesterol" in question:
            result = execute_query(
                "heart_disease.db",
                "SELECT AVG(chol) FROM heart_disease_records"
            )
            return f"The average cholesterol level is {result[0][0]:.2f}."

        if "distribution" in question or "target" in question:
            result = execute_query(
                "heart_disease.db",
                """
                SELECT target, COUNT(*)
                FROM heart_disease_records
                GROUP BY target
                """
            )
            return f"Heart disease target distribution: {result}"

        return "I can provide record counts, average age, average cholesterol, and target distribution from the Heart Disease dataset."

    except Exception as error:
        return f"Heart Disease database error: {error}"


@tool("CancerDBTool")
def cancer_db_tool(question: str) -> str:
    """Retrieve statistics and information from the Cancer dataset."""

    question = question.lower()

    try:
        if any(word in question for word in ["count", "number", "how many", "records"]):
            result = execute_query(
                "cancer.db",
                "SELECT COUNT(*) FROM cancer_records"
            )
            return f"The Cancer dataset contains {result[0][0]} records."

        if "average age" in question or "mean age" in question:
            result = execute_query(
                "cancer.db",
                "SELECT AVG(Age) FROM cancer_records"
            )
            return f"The average age is {result[0][0]:.2f} years."

        if "average bmi" in question or "mean bmi" in question:
            result = execute_query(
                "cancer.db",
                "SELECT AVG(BMI) FROM cancer_records"
            )
            return f"The average BMI is {result[0][0]:.2f}."

        if "diagnosis" in question or "distribution" in question:
            result = execute_query(
                "cancer.db",
                """
                SELECT Diagnosis, COUNT(*)
                FROM cancer_records
                GROUP BY Diagnosis
                """
            )
            return f"Cancer diagnosis distribution: {result}"

        return "I can provide record counts, average age, average BMI, and diagnosis distribution from the Cancer dataset."

    except Exception as error:
        return f"Cancer database error: {error}"
