import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Configure OpenRouter API
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def ask_llm(subjects, agent_name="agent_1"):
    summary = "\n".join([f"- {sub}" for sub in subjects])
    prompt = f"""
You are {agent_name}. You’ve been assigned the following email subjects:

{summary}

You're feeling tired. Should you process these emails now or postpone them? Prioritize any urgent items (e.g., jobs, meetings, alerts).
"""

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[{"role": "user", "content": prompt.strip()}]
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    example_subjects = [
        "New Interview Slot: Software Engineer",
        "Meeting scheduled for Friday",
        "LinkedIn newsletter: AI news"
    ]
    decision = ask_llm(example_subjects, agent_name="agent_1")
    print("🤖 LLM Response:\n", decision)
