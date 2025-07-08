from read_emails import fetch_primary_subjects
import requests

AGENTS = ["agent_1", "agent_2", "agent_3"]
MCP_SERVER = "http://127.0.0.1:8000/assign_emails"

if __name__ == "__main__":
    subjects = fetch_primary_subjects(9)
    response = requests.post(MCP_SERVER, json={
        "subjects": subjects,
        "agents": AGENTS
    })
    data = response.json()

    print("📬 Email Assignments:")
    for agent, assigned in data.items():
        print(f"\n🔹 {agent}:")
        for subject in assigned:
            print(f"   - {subject}")