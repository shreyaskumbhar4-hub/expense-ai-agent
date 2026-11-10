from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import sqlite3

from src import database
from src.agent import run_agent
from src.analytics import get_category_spending
from src.insights import get_spending_insights
from src.gamification import get_user_gamification_stats

app = FastAPI(title="Expense AI Agent")


class ChatRequest(BaseModel):
    user_id: int
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def home():
    return FileResponse("src/static/index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = run_agent(request.message, request.user_id)
    return {"response": response}


@app.get("/api/dashboard/{user_id}")
def get_dashboard_data(user_id: int):
    try:
        # 1. Fetch category analytics breakdown
        analytics_data = get_category_spending(user_id=user_id)
        
        # 2. Fetch spending insights and totals
        insights_data = get_spending_insights(user_id=user_id)

        gamification_data = get_user_gamification_stats(user_id=user_id)
        
        # 3. Fetch current wallet balance / total income
        conn = sqlite3.connect("database/expense_tracker.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(amount) as total_income FROM income WHERE user_id = ?", (user_id,))
        income_res = cursor.fetchone()
        total_income = income_res["total_income"] if income_res and income_res["total_income"] else 0.0
        
        conn.close()
        
        total_spent = insights_data["total_spent"]
        current_balance = total_income - total_spent
        
        return {
            "status": "success",
            "user_id": user_id,
            "wallet": {
                "total_income": total_income,
                "total_spent": total_spent,
                "current_balance": current_balance
            },
            "gamification": gamification_data,
            "insights": insights_data,
            "category_breakdown": analytics_data["breakdown"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))