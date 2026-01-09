import os
import json

try:
    import openai
except Exception:
    openai = None

PROMPT_TEMPLATE = """
You are an expert lab assistant. Given the following transcript and detected events, extract a structured, stepwise experimental protocol.
Return ONLY valid JSON that matches this schema:
{
  "steps": [
    {"step_number": int, "start_ts": "00:00:05", "end_ts": "00:00:09", "action": "Add Reagent A", "details": "10 µL Reagent A to tube 1", "reagents": [{"name":"Reagent A","amount":"10 µL","confidence":0.9}], "equipment": [{"name":"P10 pipette","confidence":0.9}], "notes":""}
  ],
  "reagents": [{"name":"Reagent A","amount":"10 µL","confidence":0.9}],
  "equipment": [{"name":"P10 pipette","confidence":0.9}],
  "assumptions": ["Any assumptions the model made"]
}

Transcript:
{transcript}

Detected events (json):
{events}

Produce a concise but complete protocol in the JSON schema above. Do not add extraneous text.
"""


def synthesize_structured(transcript: str, events: dict) -> dict:
    # If OpenAI available and API key present, call it
    if openai is not None and os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = PROMPT_TEMPLATE.format(transcript=transcript, events=json.dumps(events))
        try:
            resp = openai.ChatCompletion.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.0,
            )
            content = resp['choices'][0]['message']['content']
            # try parse JSON
            parsed = json.loads(content)
            return parsed
        except Exception:
            # fall through to fallback
            pass

    # fallback: naive extraction
    steps = []
    reagents = []
    equipment = []
    assumptions = []
    lines = transcript.split('\n') if transcript else []
    step_no = 1
    for i, line in enumerate(lines):
        text = line.strip()
        if not text:
            continue
        steps.append({
            "step_number": step_no,
            "start_ts": "",
            "end_ts": "",
            "action": text[:100],
            "details": text,
            "reagents": [],
            "equipment": [],
            "notes": "(auto-generated, verify)"
        })
        step_no += 1
    return {"steps": steps, "reagents": reagents, "equipment": equipment, "assumptions": assumptions}
