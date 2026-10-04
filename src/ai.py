from google import genai
import json
from datetime import date

client = genai.Client()


def understand_expense(text):
    today = date.today().isoformat()

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""
You are an expense tracking assistant.

Today is {today}.

Extract the expense from the user's message.

Return ONLY valid JSON in this exact format:

{{
    "amount": number,
    "category": "string",
    "date": "YYYY-MM-DD"
}}

Rules:
- Convert the amount to a number.
- Convert relative dates such as "today" into YYYY-MM-DD.
- If the amount is missing, return null.
- If the date is missing, return null.
- Do not invent information.

User message:
{text}
"""
    )

    return json.loads(response.text)