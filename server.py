# server.py
from fastapi import FastAPI
from fastmcp.client import MCPClient
from pydantic import BaseModel

app = FastAPI()
client = MCPClient(server_url="http://localhost:3333")  # MCP server must be running separately

class EmailAssignRequest(BaseModel):
    subjects: list[str]
    agents: list[str]

@app.post("/assign_emails")
def assign_emails(req: EmailAssignRequest):
    tools = [{"name": "email_sorter", "description": "Sort emails by importance"}]

    task_prompt = "Distribute the following email subjects among agents fairly:\n" + \
                  "\n".join(f"{i+1}. {s}" for i, s in enumerate(req.subjects))

    result = client.plan_and_assign(
        prompt=task_prompt,
        tools=tools,
        agents=req.agents,
    )

    return result
