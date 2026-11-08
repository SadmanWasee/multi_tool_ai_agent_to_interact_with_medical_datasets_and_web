
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled
)

from tools.database_tools import (
    heart_disease_db_tool,
    cancer_db_tool
)

from tools.medical_web_search_tool import medical_web_search_tool


# Disable OpenAI cloud tracing because we are using Ollama locally
set_tracing_disabled(True)


# Connect to Ollama's OpenAI-compatible API
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Configure the local Qwen model
local_model = OpenAIChatCompletionsModel(
    model="qwen2.5:3b",
    openai_client=ollama_client
)


# Wrap LangChain tools for OpenAI Agents SDK

@function_tool(
    name_override="HeartDiseaseDBTool",
    description_override=(
        "Query the Heart Disease SQLite dataset for records, "
        "statistics, counts, averages and numerical information."
    ),
    strict_mode=False
)
def heart_database_tool(question: str) -> str:
    """Execute a question against the Heart Disease database."""
    return heart_disease_db_tool.invoke({"question": question})


@function_tool(
    name_override="CancerDBTool",
    description_override=(
        "Query the Cancer SQLite dataset for records, "
        "statistics, counts, averages and numerical information."
    ),
    strict_mode=False
)
def cancer_database_tool(question: str) -> str:
    """Execute a question against the Cancer database."""
    return cancer_db_tool.invoke({"question": question})


@function_tool(
    name_override="MedicalWebSearchTool",
    description_override=(
        "Search reliable web sources for general medical knowledge, "
        "including definitions, symptoms, causes, prevention and treatments. "
        "Do not use for statistics from the project datasets."
    ),
    strict_mode=False
)
def medical_search_tool(question: str) -> str:
    """Search the web for general medical information."""
    return medical_web_search_tool.invoke({"question": question})


# Define the main AI agent
medical_agent = Agent(
    name="Medical Multi-Tool AI Agent",

    instructions="""
    You are a medical information assistant connected to two medical
    datasets and a general medical web search tool.

    You have three tools:

    1. HeartDiseaseDBTool:
       Use this tool for questions about statistics, records,
       numerical information and data from the Heart Disease dataset.

    2. CancerDBTool:
       Use this tool for questions about statistics, records,
       numerical information and data from the Cancer dataset.

    3. MedicalWebSearchTool:
       Use this tool for general medical knowledge, including
       definitions, symptoms, causes, prevention and treatments.

    ROUTING RULES:

    - Heart disease dataset questions must use HeartDiseaseDBTool.
    - Cancer dataset questions must use CancerDBTool.
    - General medical knowledge questions must use MedicalWebSearchTool.
    - Never use web search to answer questions about dataset statistics.
    - Never use database tools to answer general medical questions.
    - If a question requires both dataset statistics and general
      medical knowledge, use the appropriate tools for each part.

    RESPONSE RULES:

    - Provide clear, concise, natural-language answers.
    - Use actual tool results rather than inventing statistics.
    - Do not confuse sample database rows with total record counts.
    - Clearly distinguish dataset findings from established medical facts.
    - Dataset labels are not clinical diagnoses.
    - Do not diagnose patients or prescribe medication.
    - For medical advice, encourage consultation with qualified
      healthcare professionals.
    - Preserve source URLs when answering from web search results.
    """,

    model=local_model,

    tools=[
        heart_database_tool,
        cancer_database_tool,
        medical_search_tool
    ]
)


# Function to run the agent
async def ask_medical_agent(question: str) -> str:

    result = await Runner.run(
        medical_agent,
        question
    )

    return result.final_output
