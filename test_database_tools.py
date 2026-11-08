
from tools.database_tools import (
    heart_disease_db_tool,
    cancer_db_tool
)


def main():
    print("\nTesting Heart Disease Database...")

    heart_result = heart_disease_db_tool.invoke({
        "question": "How many records are available?"
    })

    print("Answer:", heart_result)

    print("\nTesting Cancer Database...")

    cancer_result = cancer_db_tool.invoke({
        "question": "How many records are available?"
    })

    print("Answer:", cancer_result)

    print("\nTesting Cancer Average Age...")

    age_result = cancer_db_tool.invoke({
        "question": "What is the average age?"
    })

    print("Answer:", age_result)


if __name__ == "__main__":
    main()
