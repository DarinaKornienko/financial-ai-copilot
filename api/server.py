import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv() 

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.financial_agent import agent_executor

app = FastAPI(title="RiskIntel API")

#  session_id to track conversations
class AnalyzeRequest(BaseModel):
    query: str
    session_id: str 

@app.post("/analyze")
async def analyze_company(request: AnalyzeRequest):
    print(f"\nAPI Request [Thread: {request.session_id}]: {request.query}")
    try:
        # Pass the session ID into the agent's configuration
        config = {"configurable": {"thread_id": request.session_id}}
        
        response = agent_executor.invoke(
            {"messages": [("user", request.query)]},
            config=config # The agent now saves/loads history using this ID
        )
        
        final_answer = response["messages"][-1].content
        
        return {
            "status": "success",
            "analysis": final_answer
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Agent Error")

if __name__ == "__main__":
    import uvicorn
    print("Starting API Server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)