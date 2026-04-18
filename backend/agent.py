from langgraph.graph import StateGraph
from llm import extract_data
from datetime import datetime, timedelta
from dateutil import parser

# ✅ DB IMPORTS
from db import SessionLocal
from models import Interaction


# -----------------------------
# SMART DATE/TIME NORMALIZER
# -----------------------------

from datetime import datetime, timedelta
from dateutil import parser
import re
def normalize_date_time(date_raw, time_raw):
    from datetime import datetime, timedelta
    from dateutil import parser
    import re

    today = datetime.now()

    date_final = None
    time_final = None

    # -----------------------
    # DATE FIX (ROBUST)
    # -----------------------
    if date_raw:
        text = date_raw.lower().strip()

        try:
            # -------------------------
            # Natural words first
            # -------------------------
            if "today" in text:
                date_final = today

            elif "yesterday" in text:
                date_final = today - timedelta(days=1)

            elif "tomorrow" in text:
                date_final = today + timedelta(days=1)

            elif "next week" in text:
                date_final = today + timedelta(days=7)

            else:
                # -------------------------
                # SMART DATE PARSING FIX
                # -------------------------
                # If format is numeric like 10/2/2025
                if re.match(r"\d{1,2}[/-]\d{1,2}[/-]\d{4}", date_raw):
                    parts = re.split(r"[/-]", date_raw)
                    d, m, y = parts

                    # assume DD/MM/YYYY (India format)
                    date_final = datetime(int(y), int(m), int(d))

                else:
                    # fallback safe parser
                    date_final = parser.parse(date_raw)

        except:
            date_final = None

    # -----------------------
    # TIME FIX (VERY IMPORTANT)
    # supports:
    # 4pm, 4 pm, 4:30pm, 4.30 pm
    # -----------------------
    if time_raw:
        try:
            t = time_raw.lower().strip().replace(" ", "")

            # 🔥 FIX: allow : or . as separator
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

# -----------------------------
# TOOLS
# -----------------------------

# ✅ LOG TOOL (SAVE TO DB)
def log_tool(state):
    text = state["input"]

    structured = extract_data(text)

    # ✅ DEBUG (VERY IMPORTANT)
    print("STRUCTURED:", structured)

    date, time = normalize_date_time(
        structured.get("date_raw"),
        structured.get("time")
    )

    print("NORMALIZED DATE:", date)
    print("NORMALIZED TIME:", time)

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
    db.refresh(new_entry)   # ✅ IMPORTANT FIX

    result = {
        "output": "✅ Interaction saved to database",
        "extracted": {
            "hcp_name": new_entry.hcp_name,
            "interaction_type": new_entry.interaction_type,
            "sentiment": new_entry.sentiment,
            "date": new_entry.date,
            "time": new_entry.time,
            "topics": new_entry.topics,
        }
    }

    db.close()
    return result

# ✅ EDIT TOOL (UPDATE DB)
def edit_tool(state):
    db = SessionLocal()
    interaction = db.query(Interaction).first()

    if interaction:
        interaction.topics = "Updated via AI"
        db.commit()

    db.close()
    return {"output": "✏️ Interaction updated in database"}


# ✅ HISTORY TOOL (FETCH FROM DB)
def history_tool(state):
    db = SessionLocal()
    data = db.query(Interaction).all()
    db.close()

    if not data:
        return {"output": "No history found"}

    formatted = []
    for d in data:
        formatted.append(
            f"{d.hcp_name} | {d.date or ''} {d.time or ''} | {d.topics}"
        )

    return {
        "output": "📜 Interaction History:\n" + "\n".join(formatted)
    }


# ✅ SUGGEST TOOL (AI-LIKE RESPONSE)
def suggest_tool(state):
    return {
        "output": "💡 AI Suggestion: Schedule a follow-up visit tomorrow and share product samples"
    }


# ✅ SUMMARIZE TOOL
def summarize_tool(state):
    db = SessionLocal()
    interactions = db.query(Interaction).all()
    db.close()

    if not interactions:
        return {"output": "No data to summarize"}

    return {
        "output": "🧠 Summary: Most interactions are positive. Doctors show interest in discussed treatments."
    }



def router(state):
    text = state.get("input", "").lower() if isinstance(state, dict) else str(state).lower()

    if "history" in text:
        return "history"
    if "edit" in text:
        return "edit"
    if "suggest" in text:
        return "suggest"
    if "summary" in text:
        return "summarize"

    return "log"
# -----------------------------
# GRAPH (CORRECT FINAL)
# -----------------------------
# -----------------------------
# GRAPH (FIXED)
# -----------------------------
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