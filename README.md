# AI-First CRM – HCP Module (Log Interaction Screen)

## 📌 Overview

This project is an AI-first CRM system for Healthcare Professional (HCP) interaction logging. It enables field representatives to log interactions using either:

* 💬 Conversational AI chat (LangGraph + LLM)
* 🧾 Structured CRM form (React UI)

The system extracts structured medical sales interaction data from natural language and stores it in a database.

---

## 🚀 Key Features

* 💬 Dual input system: Chat + Form-based logging
* 🤖 LLM-powered extraction using Groq (Llama-3.3-70b / Gemma2-9B-IT)
* 🧠 LangGraph agent orchestration
* 📅 Smart date handling (today, yesterday, natural dates, DD/MM/YYYY)
* ⏰ Smart time parsing (4pm, 4.30 pm, 16:30)
* 🏥 HCP interaction tracking (doctor name, sentiment, topics)
* 🗄️ SQLite database storage (SQLAlchemy ORM)
* ⚛️ React frontend with real-time CRM autofill
* 🔄 AI-driven form auto-population from chat

---

## 🏗️ Tech Stack

### Frontend

* React.js
* useState / useEffect (state handling)
* Axios (API calls)
* Vanilla CSS styling

### Backend

* FastAPI
* Python
* SQLAlchemy ORM
* SQLite database

### AI Layer

* LangGraph (agent routing system)
* Groq API
* Llama 3.3 70B / Gemma 2 9B IT

---

## 🧠 LangGraph Agent Architecture

The LangGraph agent controls how user input flows through tools.

### Workflow

1. User sends input (chat or structured form)
2. LLM extracts structured medical CRM data
3. Router decides tool execution path
4. Tool processes data
5. Data stored in database
6. Response returned to frontend

---

## 🛠️ LangGraph Tools Implemented

### 1. Log Interaction Tool

* Extracts structured HCP interaction data
* Normalizes date/time
* Saves data into SQLite database

### 2. Edit Interaction Tool

* Updates existing interaction records
* Used for corrections

### 3. History Tool

* Fetches all past HCP interactions
* Returns formatted interaction logs

### 4. Suggest Tool

* AI-based sales suggestion engine
* Provides next-step recommendations

### 5. Summarize Tool

* Summarizes interaction trends
* Identifies sentiment patterns

---

## 🧾 Data Model (Backend)

### Interaction Table

```python
id: int (primary key)
hcp_name: string
interaction_type: string
sentiment: string
date: string (YYYY-MM-DD)
time: string (HH:MM)
topics: string
```

---

## 🔥 LLM Extraction Example

### Input:

> Met Dr Smith today at 4.30 pm, discussed cancer drug, very negative

### Output:

```json
{
  "hcp_name": "Dr Smith",
  "interaction_type": "Meeting",
  "sentiment": "Negative",
  "date_raw": "today",
  "time": "4.30 pm",
  "topics": "cancer drug discussion"
}
```

---

## ⚙️ Backend Logic (Important Highlights)

### 🔹 Smart Date Normalization

* today → current date
* yesterday → current date - 1
* DD/MM/YYYY parsing supported

### 🔹 Smart Time Normalization

* 4pm → 16:00
* 4.30 pm → 16:30
* 12-hour → 24-hour conversion

---

## 💬 Frontend Features

### CRM Form

* Auto-filled from AI chat
* Editable fields:

  * HCP Name
  * Interaction Type
  * Date
  * Time
  * Topics
  * Sentiment

### Chat System

* User sends natural language
* AI extracts structured CRM data
* Automatically fills form fields

---

## 🔄 Integration Flow

Frontend (React)
↓
FastAPI (/chat endpoint)
↓
LangGraph Agent
↓
LLM (Groq)
↓
Extraction + Normalization
↓
SQLite DB
↓
Response + UI Autofill

---

## 📦 Setup Instructions

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

---

## 🔐 Environment Variables

Create `.env` in backend:

```
GROQ_API_KEY=your_key_here
```

---

## 🎯 Project Highlights

* Real-world AI CRM simulation
* Medical sales workflow automation
* LangGraph-based agent design
* Robust NLP parsing for messy human input
* Full-stack integration (React + FastAPI + LLM)

---

## 📌 Author

Md Sahabuddin

---

## ✅ Status

✔ Backend working
✔ Frontend working
✔ LangGraph agent active
✔ AI extraction stable
✔ Ready for submission
