# AI-First CRM – HCP Module (Log Interaction Screen)

## 📌 Overview

This project is an AI-first CRM system designed for Healthcare Professionals (HCP) interaction logging. It allows field representatives to log interactions using either a structured form or a conversational chat interface powered by an AI agent built with LangGraph and LLMs.

The system extracts structured insights (HCP name, interaction type, sentiment, date, time, and topics) from natural language inputs and stores them in a database.

---

## 🚀 Features

* 💬 Dual input system: Chat + Structured form
* 🤖 AI-powered interaction extraction using LLM (Groq / Gemma2-9B-IT)
* 🔗 LangGraph-based agent workflow
* 🧠 Automatic entity extraction (HCP, sentiment, topics, etc.)
* 📅 Natural date/time parsing (today, yesterday, specific date)
* 🗄️ Database storage (MySQL/PostgreSQL compatible)
* ⚛️ React frontend with clean UI
* ⚡ FastAPI backend

---

## 🏗️ Tech Stack

### Frontend

* React.js
* Redux (state management)
* Axios
* Google Fonts (Inter)

### Backend

* FastAPI
* Python
* SQLAlchemy ORM

### AI Layer

* LangGraph (agent orchestration)
* Groq API
* Llama 3 / Gemma 2 9B IT

### Database

* PostgreSQL / MySQL

---

## 🧠 LangGraph Agent Design

The LangGraph agent is responsible for orchestrating the entire interaction lifecycle.

### Workflow:

1. User input (chat or form)
2. LLM parsing & extraction
3. Tool execution
4. Data normalization
5. Database logging
6. Response generation

---

## 🛠️ LangGraph Tools

### 1. Log Interaction Tool

* Extracts structured fields using LLM
* Normalizes date/time
* Stores interaction in database

### 2. Edit Interaction Tool

* Allows modification of existing HCP logs
* Updates database records safely

### 3. Fetch HCP History Tool

* Retrieves past interactions of a doctor/HCP

### 4. Sentiment Analysis Tool

* Classifies interaction as Positive / Neutral / Negative

### 5. Topic Extraction Tool

* Extracts key discussion topics from conversation

---

## 🧾 Example Interaction

**Input:**

> Met Dr Smith today at 4:30 pm, discussed cancer drug progress, very positive discussion.

**Extracted Output:**

```json
{
  "hcp_name": "Dr Smith",
  "interaction_type": "Meeting",
  "sentiment": "Positive",
  "date": "2026-04-18",
  "time": "16:30",
  "topics": "cancer drug progress"
}
```

---

## ⚙️ Setup Instructions

### 1. Clone repository

```bash
git clone https://github.com/<your-username>/ai-crm-hcp-module.git
cd ai-crm-hcp-module
```

### 2. Backend setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm start
```

---

## 🔐 Environment Variables

Create a `.env` file in backend:

```
GROQ_API_KEY=your_api_key_here
DATABASE_URL=your_database_url
```

---

## 📊 Architecture

Frontend (React + Redux)
↓
FastAPI Backend
↓
LangGraph Agent
↓
LLM (Groq / Llama / Gemma)
↓
Database (PostgreSQL/MySQL)

---

## 🎯 Key Learning

* AI-first CRM design approach
* LangGraph workflow orchestration
* LLM-based structured data extraction
* Real-world healthcare CRM simulation

---

## 📌 Author

Md Sahabuddin

---

## ✅ Status

✔ Backend integrated
✔ Frontend working
✔ AI agent functional
✔ Ready for submission
