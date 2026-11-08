
from tools.medical_web_search_tool import medical_web_search_tool

print("\nTesting Medical Web Search Tool...")

result = medical_web_search_tool.invoke({
    "question": "What is hypertension and what are its common symptoms?"
})

print("\nSearch Results:")
print(result)

print("\nMedical web search test completed!")
