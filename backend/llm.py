import json
from pydoc import text
import re
import os
from groq import Groq

client = Groq(api_key="YOUR_GROQ_API_KEY")

def clean_json(text):
    try:
        text = re.sub(r"```json|```", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None


def extract_data(text):
    prompt = f"""
You are an expert AI assistant for a pharmaceutical CRM system.

Extract structured interaction data.

Return ONLY JSON:

{{
  "hcp_name": "",
  "interaction_type": "",
  "sentiment": "",
  "date_raw": "",
  "time": "",
  "topics": ""
}}

RULES:
- Extract doctor name (e.g., Dr Mehta)
- interaction_type: Meeting / Call / Visit
- sentiment: Positive / Neutral / Negative
- date_raw: today / yesterday / actual date
- time: like 4pm
- topics: short summary

Example:
Met Dr Mehta today at 4pm, discussed cancer drug, very positive

Output:
{{
  "hcp_name": "Dr Mehta",
  "interaction_type": "Meeting",
  "sentiment": "Positive",
  "date_raw": "today",
  "time": "4pm",
  "topics": "cancer drug discussion"
}}

Text:
{text}
"""

    res = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    content = res.choices[0].message.content

    print("RAW LLM RESPONSE:", content)

    parsed = clean_json(content)

    print("PARSED JSON:", parsed)

    # ✅ If LLM works
    if parsed:
        return parsed
    # 🔥 FALLBACK
# 🔥 STRONG FALLBACK
# 🔥 FALLBACK (STRONG VERSION)
# 🔥 FALLBACK (FINAL)
    hcp = re.search(r"(Dr\.?\s+[A-Z][a-z]+)", text)
    time = re.search(r"(\d{1,2}\s?(?:am|pm))", text, re.IGNORECASE)
    topic_match = re.search(r"discussed (.*?)(,|$)", text, re.IGNORECASE)

    # 👉 CLEAN TOPIC
    clean_topic = ""
    if topic_match:
        clean_topic = topic_match.group(1).strip()
        clean_topic = clean_topic.replace("discussion", "")
        clean_topic = clean_topic.replace("discussed", "")
        clean_topic = clean_topic.strip()

    return {
        "hcp_name": hcp.group(1) if hcp else "Dr Unknown",
        "interaction_type": "Meeting",
        "sentiment": "Positive" if "positive" in text.lower() else "Neutral",
        "date_raw": "today" if "today" in text.lower() else "",
        "time": time.group(1) if time else "",
        "topics": topic_match.group(1) if topic_match else text[:120]
    }