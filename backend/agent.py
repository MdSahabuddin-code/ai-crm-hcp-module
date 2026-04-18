from langgraph.graph import StateGraph
from llm import extract_data
from datetime import datetime, timedelta
from dateutil import parser
import re

from db import SessionLocal
from models import Interaction


# =====================================================
# SMART NORMALIZER (FIXED)
# =====================================================
def normalize_date_time(date_raw, time_raw):
    today = datetime.now()

    date_final = None
    time_final = None

    # ---------------- DATE ----------------
    if date_raw:
        text = str(date_raw).lower().strip()

        try:
            if "today" in text:
                date_final = today

            elif "yesterday" in text:
                date_final = today - timedelta(days=1)

            elif "tomorrow" in text:
                date_final = today + timedelta(days=1)

            elif "next week" in text:
                date_final = today + timedelta(days=7)

            else:
                match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})", text)

                if match:
                    d, m, y = re.split(r"[/-]", match.group(1))
                    date_final = datetime(int(y), int(m), int(d))
                else:
                    date_final = parser.parse(text)

        except:
            date_final = None

    # ---------------- TIME ----------------
    if time_raw:
        try:
            t = str(time_raw).lower().replace(" ", "")

            match = re.match(r"(\d{1,2})([:.](\d{2}))?(am|pm)?", t)

            if match:
                hour = int(match.group(1))
                minute = int(match.group(3) or 0)
                mer = match.group(4)

                if mer == "pm" and hour != 12:
                    hour += 12
                if mer == "am" and hour == 12:
                    hour = 0

                time_final = f"{hour:02d}:{minute:02d}"
            else:
                time_final = parser.parse(time_raw).strftime("%H:%M")

        except:
            time_final = None

    return (
        date_final.strftime("%Y-%m-%d") if date_final else None,
        time_final
    )


# =====================================================
# LOG TOOL
# =====================================================
def log_tool(state):
    text = state["input"]
    structured = extract_data(text)

    date, time = normalize_date_time(
        structured.get("date_raw"),
        structured.get("time")
    )

    db = SessionLocal()

    new_entry = Interaction(
        hcp_name=structured.get("hcp_name"),
        interaction_type=structured.get("interaction_type"),
        sentiment=structured.get("sentiment"),
        date=date,
        time=time,
        topics=structured.get("topics")
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    # ✅ STORE DATA BEFORE closing session (important)
    result_data = {
        "hcp_name": new_entry.hcp_name,
        "interaction_type": new_entry.interaction_type,
        "sentiment": new_entry.sentiment,
        "date": new_entry.date,
        "time": new_entry.time,
        "topics": new_entry.topics,
    }

    db.close()

    return {
        "output": "✅ Interaction saved to database",
        "extracted": result_data   # ✅ THIS FIXES YOUR UI
    }

# =====================================================
# EDIT TOOL (FULL FIX)
# =====================================================
def edit_tool(state):
    db = SessionLocal()
    text = state.get("input", "").lower()

    interaction_id = state.get("interaction_id")

    if interaction_id:
        interaction = db.query(Interaction).filter_by(id=interaction_id).first()
    else:
        interaction = db.query(Interaction).order_by(Interaction.id.desc()).first()

    if not interaction:
        return {"output": "No interaction found"}

    # ---------------- NAME ----------------
    dr_match = re.search(r"dr\.?\s+[a-z]+", text, re.IGNORECASE)
    if dr_match:
        interaction.hcp_name = dr_match.group()

    # ---------------- TOPICS ----------------
    if "topic" in text or "product" in text:
        interaction.topics = text.replace("edit last interaction", "").strip()

    # ---------------- TIME ----------------
    time_match = re.search(r"(\d{1,2})([:.]?\d{2})?\s?(am|pm)", text)

    if time_match:
        hour = int(time_match.group(1))

        minute_raw = time_match.group(2)
        minute = int(minute_raw.replace(":", "").replace(".", "")) if minute_raw else 0

        mer = time_match.group(3)

        if mer == "pm" and hour != 12:
            hour += 12
        if mer == "am" and hour == 12:
            hour = 0

        interaction.time = f"{hour:02d}:{minute:02d}"

    # ---------------- DATE ----------------
    date_match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})", text)

    if date_match:
        try:
            d, m, y = re.split(r"[/-]", date_match.group(1))
            interaction.date = datetime(int(y), int(m), int(d)).strftime("%Y-%m-%d")
        except:
            pass

    elif "yesterday" in text:
        interaction.date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    elif "today" in text:
        interaction.date = datetime.now().strftime("%Y-%m-%d")

    elif "tomorrow" in text:
        interaction.date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    db.commit()
    db.refresh(interaction)  # ✅ VERY IMPORTANT

    # ✅ SAVE DATA BEFORE closing DB
    updated_data = {
        "hcp_name": interaction.hcp_name,
        "interaction_type": interaction.interaction_type,
        "sentiment": interaction.sentiment,
        "date": interaction.date,
        "time": interaction.time,
        "topics": interaction.topics,
    }

    db.close()

    return {
        "output": "✏️ Interaction updated successfully",
        "updated": updated_data   # ✅ THIS FIXES FRONTEND
    }

# =====================================================
# HISTORY TOOL
# =====================================================
def history_tool(state):
    db = SessionLocal()
    data = db.query(Interaction).all()
    db.close()

    formatted = [
        f"\n{d.hcp_name} | {d.date or ''} {d.time or ''} | {d.topics}"
        for d in data
    ]

    return {"output": "📜 Interaction History:\n" + "\n".join(formatted)}


# =====================================================
# SUGGEST TOOL
# =====================================================
def suggest_tool(state):
    return {"output": "💡 AI Suggestion: Schedule follow-up visit and share samples"}


# =====================================================
# SUMMARY TOOL
# =====================================================
def summarize_tool(state):
    db = SessionLocal()
    data = db.query(Interaction).all()
    db.close()

    return {"output": "🧠 Summary: Mostly positive doctor interactions with strong engagement."}


# =====================================================
# ROUTER
# =====================================================
def router(state):
    text = state.get("input", "").lower()

    if "history" in text:
        return "history"
    if "edit" in text:
        return "edit"
    if "suggest" in text:
        return "suggest"
    if "summary" in text:
        return "summarize"

    return "log"


# =====================================================
# LANGGRAPH SETUP
# =====================================================
builder = StateGraph(dict)

builder.add_node("log", log_tool)
builder.add_node("edit", edit_tool)
builder.add_node("history", history_tool)
builder.add_node("suggest", suggest_tool)
builder.add_node("summarize", summarize_tool)

builder.set_conditional_entry_point(
    router,
    {
        "log": "log",
        "edit": "edit",
        "history": "history",
        "suggest": "suggest",
        "summarize": "summarize"
    }
)

graph = builder.compile()
