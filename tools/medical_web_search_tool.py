
import os

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

# Load environment variables
load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY is missing from the .env file")


# Initialize Tavily search
tavily_search = TavilySearch(
    max_results=5,
    topic="general",
    include_answer=True
)


@tool("MedicalWebSearchTool")
def medical_web_search_tool(question: str) -> str:
    """
    Search the web for general medical knowledge,
    including disease definitions, symptoms, causes,
    prevention and treatment information.

    Do not use this tool for statistics or records
    from the project's medical datasets.
    """

    try:
        search_query = (
            f"Medical information from reliable healthcare sources: {question}"
        )

        result = tavily_search.invoke({
            "query": search_query
        })

        return str(result)

    except Exception as error:
        return f"Medical web search failed: {error}"
