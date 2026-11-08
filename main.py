import asyncio
from orchestration.main_agent import ask_medical_agent


async def main():
    print("=" * 55)
    print("       MEDICAL MULTI-TOOL AI AGENT")
    print("=" * 55)
    print("Ask questions about the medical datasets or general")
    print("medical knowledge.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("\nGoodbye!")
            break

        if not question:
            continue

        try:
            answer = await ask_medical_agent(question)
            print(f"\nAgent: {answer}\n")

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    asyncio.run(main())