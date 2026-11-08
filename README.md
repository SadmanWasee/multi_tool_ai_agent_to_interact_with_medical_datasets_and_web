# Medical Multi-Tool AI Agent

An AI-powered multi-tool agent that answers questions about medical datasets and general medical knowledge by intelligently selecting between local SQLite databases and web search.

## Overview

This project implements a multi-tool AI agent capable of interacting with structured medical datasets and retrieving general medical information from the web.

The agent uses **Qwen 2.5 (3B)** through Ollama as its local language model and the **OpenAI Agents SDK** for agent orchestration. LangChain tools provide access to medical databases and web search functionality.

The system distinguishes between questions requiring dataset analysis and questions requiring general medical knowledge, routing each query to the appropriate tool.

## Features

- **Heart Disease Database:** Retrieves statistics and information from the Heart Disease dataset.
- **Cancer Database:** Retrieves statistics and information from the Cancer dataset.
- **Medical Web Search:** Searches the web for general medical knowledge, symptoms, causes, prevention, and treatment information.
- **Intelligent Tool Selection:** Automatically determines which tool should handle a user's question.
- **Local LLM Integration:** Uses Ollama and Qwen 2.5 (3B), avoiding dependence on paid LLM APIs.
- **SQLite Integration:** Stores medical datasets in local SQLite databases.
- **Command-Line Interface:** Provides an interactive interface for asking questions.

## System Architecture

The application follows a tool-based agent architecture.

```text
                    User Query
                        |
                        v
              +--------------------+
              |   Main AI Agent    |
              | OpenAI Agents SDK  |
              |   Qwen 2.5 (3B)    |
              +--------------------+
                        |
                Tool Selection
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
   +-------------+ +-------------+ +----------------+
   | Heart Disease| | Cancer      | | Medical Web    |
   | Database Tool| | Database Tool| | Search Tool    |
   +-------------+ +-------------+ +----------------+
          |             |             |
          v             v             v
   +-------------+ +-------------+ +----------------+
   | Heart SQLite| | Cancer SQLite| | Tavily Search   |
   | Database    | | Database     | | API             |
   +-------------+ +-------------+ +----------------+
          |             |             |
          +-------------+-------------+
                        |
                        v
                Agent Response
                        |
                        v
                       User
```

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenAI Agents SDK | Main agent orchestration and tool calling |
| LangChain Core | Tool definitions |
| SQLite | Medical dataset storage |
| Ollama | Local LLM execution |
| Qwen 2.5 (3B) | Language model |
| LangChain Tavily | Web search integration |
| Tavily API | Medical information retrieval |
| python-dotenv | Environment variable management |

## Datasets

The project currently integrates two medical datasets.

### 1. Heart Disease Dataset

- **Records:** 1,025
- **Database:** `heart_disease.db`
- **Table:** `heart_disease_records`
- **Source:** [Heart Disease Dataset – Kaggle](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)

The dataset contains patient information and clinical attributes used for heart disease analysis.

### 2. Cancer Dataset

- **Records:** 1,500
- **Database:** `cancer.db`
- **Table:** `cancer_records`
- **Source:** [The Cancer Data – Kaggle](https://www.kaggle.com/datasets)

The dataset contains demographic, lifestyle, and cancer-related attributes.

**Dataset limitation:** The Diabetes dataset specified in the original assignment was unavailable during implementation. Therefore, the current application supports the Heart Disease and Cancer datasets. Diabetes-related general medical questions can still be answered through the web search tool.

## Project Structure

```text
multi_tool_ai_agent_to_interact_with_medical_datasets_and_web/
│
├── data/
│   ├── heart.csv
│   └── The_Cancer_data_1500_V2.csv
│
├── databases/
│   ├── heart_disease.db
│   └── cancer.db
│
├── tools/
│   ├── __init__.py
│   ├── database_tools.py
│   └── medical_web_search_tool.py
│
├── orchestration/
│   ├── __init__.py
│   └── main_agent.py
│
├── database_setup.py
├── main.py
├── test_database_tools.py
├── test_main_agent.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Make sure you have installed:

- Python 3.12
- [Ollama](https://ollama.com/)
- Git
- A Tavily API key

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the Local Language Model

Install the Qwen 2.5 3B model using Ollama:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before launching the application.

### 5. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Tavily API key:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

You can obtain an API key from [Tavily](https://tavily.com/).

**Important:** Never commit your `.env` file or expose your API key publicly.

### 6. Initialize the Databases

Run:

```bash
python database_setup.py
```

This script processes the available CSV datasets and creates the corresponding SQLite databases.

## Running the Application

Start the interactive command-line application:

```bash
python main.py
```

The agent will accept questions until you enter `exit` or `quit`.

## Example Queries

### Heart Disease Database

**Question:**
```text
How many records are available in the heart disease dataset?
```

**Response:**
```text
The heart disease dataset contains 1025 records.
```

### Cancer Database

**Question:**
```text
What is the average age of patients in the cancer dataset?
```

**Response:**
```text
The average age of patients in the cancer dataset is 50.32 years.
```

### Cancer Statistics

**Question:**
```text
What is the average BMI in the cancer dataset?
```

**Response:**
```text
The average BMI in the cancer dataset is 27.51.
```

### Medical Web Search

**Question:**
```text
What is hypertension and what are its common symptoms?
```

**Response:**

The agent retrieves general medical information from online healthcare sources and summarizes the relevant findings.

## Testing

The project includes separate test scripts for verifying database tools and the main AI agent.

**Test database tools:**

```bash
python test_database_tools.py
```

**Test the main agent:**

```bash
python test_main_agent.py
```

The tests verify database queries, dataset statistics, tool selection, and web search functionality.

## Safety and Limitations

- The database tools use read-only SQLite queries.
- The agent is intended for educational and informational purposes, not medical diagnosis.
- General medical information is retrieved through web search and may require independent verification.
- The application does not replace professional medical advice.
- Only two medical datasets are currently integrated.
- Database queries are implemented using deterministic SQL operations rather than a language-model-driven SQL AgentExecutor.

## Future Improvements

- Integrate the Diabetes dataset.
- Add more medical datasets and database tools.
- Implement a web-based interface using React or Streamlit.
- Add conversation memory and contextual follow-up questions.
- Improve source verification and medical information retrieval.
- Introduce more advanced database querying capabilities.

## Author

**Sadman Wasee**

Computer Science and Engineering Graduate

GitHub: [SadmanWasee](https://github.com/SadmanWasee)

---

*Developed as part of the AI Engineering Course – Module 23: Building a Multi-Tool AI Agent to Interact with Medical Datasets and Web.*
