# 💰 Expense AI Agent

An AI-powered personal finance tracker built with **Python, Gemini, FastAPI, and SQLite**.

The goal of this project is to build a real AI agent that can understand natural-language financial requests, use tools to interact with financial data, and provide useful spending insights.

## ✨ Features

* Add expenses using natural language
* Add income using natural language
* View expenses and income
* Update expenses and income
* Delete expenses and income with confirmation
* Daily, weekly, monthly, and yearly spending summaries
* Current balance calculation
* Gemini-powered natural-language understanding
* AI tool calling
* Multi-step agent loop
* SQLite database
* FastAPI backend
* Simple web chat interface

## 🧠 How the AI Agent Works

```text
User
  ↓
FastAPI
  ↓
AI Agent
  ↓
Gemini
  ↓
Tool Decision
  ↓
Python Tool
  ↓
SQLite Database
  ↓
Tool Result
  ↓
Gemini
  ↓
Final Response
```

The AI model does not directly modify the database.

Instead, it requests tools such as:

```text
add_expense
get_expenses
update_expense
delete_expense
add_income
get_income
get_balance
get_daily_summary
```

The application executes those tools and sends the results back to the model.

## 🛠️ Tech Stack

* **Python**
* **Google Gemini API**
* **google-genai**
* **FastAPI**
* **SQLite**
* **Pydantic**
* **Pytest**
* **HTML/CSS/JavaScript**

## 📁 Project Structure

```text
expense-ai-agent/
│
├── src/
│   ├── main.py
│   ├── database.py
│   ├── income.py
│   ├── expense.py
│   ├── balance.py
│   ├── summary.py
│   ├── user.py
│   ├── ai.py
│   ├── agent.py
│   ├── tools.py
│   │
│   ├── test_*.py
│   └── static/
│       └── index.html
│
├── database/
│   └── expense_tracker.db
│
├── .gitignore
├── README.md
└── requirements.txt
```

## 🚀 Setup

Clone the repository:

```bash
git clone https://github.com/shreyaskumbhar4-hub/expense-ai-agent.git
cd expense-ai-agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows CMD:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Gemini API Key

Create a Gemini API key and configure it as an environment variable.

Windows CMD:

```cmd
set GEMINI_API_KEY=your_api_key
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="your_api_key"
```

Do **not** commit your API key to GitHub.

## ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn src.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## 💬 Example Requests

```text
I spent ₹250 on food today
```

```text
I received ₹5000 from freelance work today
```

```text
How much did I spend today?
```

```text
How much money do I have?
```

```text
Show me all my expenses
```

```text
Change the ₹500 expense to ₹400
```

```text
Delete the ₹50 snacks expense
```

The agent asks for confirmation before updating or deleting existing records.

## 🧪 Testing

Run all tests:

```bash
python -m pytest src
```

Or run individual tests:

```bash
python src/test_expense.py
python src/test_income.py
python src/test_balance.py
python src/test_agent.py
python src/test_tools.py
```

## 🔐 Security

The current version is a learning/demo project.

Before production deployment, the application should add:

* User authentication
* Authorization
* Secure session management
* Better API validation
* Production database configuration
* Proper secret management
* Rate limiting
* HTTPS

The current frontend uses a fixed demo user ID and should **not** be exposed publicly with real financial data.

## 🗺️ Roadmap

### Completed

* [x] SQLite database
* [x] Expense CRUD
* [x] Income CRUD
* [x] Balance calculation
* [x] Daily summary
* [x] Weekly summary
* [x] Monthly summary
* [x] Yearly summary
* [x] Gemini integration
* [x] AI tool calling
* [x] Multi-step agent loop
* [x] Confirmation flow
* [x] FastAPI backend
* [x] Web chat interface

### Next

* [ ] Daily budget
* [ ] Weekly budget
* [ ] Monthly budget
* [ ] Yearly budget
* [ ] Budget rollover
* [ ] Reserve pool
* [ ] Agent Points
* [ ] User levels
* [ ] Spending insights
* [ ] Dashboard
* [ ] Voice input
* [ ] Authentication
* [ ] Production deployment

## 🎯 Learning Goals

This project is being built as a practical way to learn:

* LLM APIs
* Prompt design
* Tool calling
* AI agents
* Agent loops
* State management
* Database integration
* API development
* Backend architecture
* AI application security

The focus is not just on making an AI chatbot, but on understanding how an AI agent interacts with real application tools and data.

## 📄 License

This project is currently intended as a personal learning project.


