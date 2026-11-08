
import asyncio

from orchestration.main_agent import ask_medical_agent


async def main():

    questions = [
        "How many records are available in the heart disease dataset?",

        "What is the average age of patients in the cancer dataset?",

        "What is hypertension and what are its common symptoms?"
    ]

    for question in questions:

        print("\n" + "=" * 65)
        print("USER QUESTION:", question)
        print("=" * 65)

        answer = await ask_medical_agent(question)

        print("\nAGENT RESPONSE:")
        print(answer)


if __name__ == "__main__":
    asyncio.run(main())
