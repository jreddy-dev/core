import os
import tempfile
from ..db import SessionLocal
from ..models import Video, ProcessingResult

# Optional imports
try:
    import whisper
except Exception:
    whisper = None

try:
    import openai
except Exception:
    openai = None


def transcribe_with_whisper(path: str):
    if whisper is None:
        return [{"start": 0.0, "end": 1.0, "text": "(transcription unavailable - whisper not installed)"}]
    model = whisper.load_model("small")
    result = model.transcribe(path)
    # Convert to simple segments
    segments = []
    for seg in result.get("segments", []):
        segments.append({"start": seg["start"], "end": seg["end"], "text": seg["text"]})
    return segments


def simple_summarize(transcript_segments):
    # naive summarization: join and take first 500 chars
    text = " ".join([s.get("text", "") for s in transcript_segments])
    return text[:1000]


def process_video(video_id: str):
    session = SessionLocal()
    v = session.query(Video).filter(Video.id == video_id).first()
    if not v:
        session.close()
        raise RuntimeError("video not found")

    path = v.url
    # transcribe
    transcripts = transcribe_with_whisper(path)
    summary = simple_summarize(transcripts)

    pr = ProcessingResult(video_id=video_id, transcripts={"segments": transcripts}, detections={}, actions={}, ocr={}, summary_text=summary)
    session.add(pr)
    v.status = "processed"
    session.add(v)
    session.commit()
    session.refresh(pr)
    session.close()
    return pr


def synthesize_protocol(video_id: str):
    session = SessionLocal()
    video = session.query(Video).filter(Video.id == video_id).first()
    if not video:
        session.close()
        raise RuntimeError("video not found")
    pr = session.query(ProcessingResult).filter(ProcessingResult.video_id == video_id).order_by(ProcessingResult.created_at.desc()).first()
    transcript = ""
    if pr and pr.transcripts:
        for s in pr.transcripts.get("segments", []):
            transcript += s.get("text", "") + "\n"

    # Use OpenAI if configured
    protocol_md = ""
    if openai is not None and os.getenv("OPENAI_API_KEY"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"Extract a stepwise protocol from the following transcript. Output markdown with numbered steps.\n\n{transcript}\n\nProtocol:" 
        try:
            resp = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=400,
                temperature=0.2,
            )
            protocol_md = resp.choices[0].text.strip()
        except Exception:
            protocol_md = "(OpenAI request failed)\n\n" + transcript[:500]
    else:
        # fallback: naive protocol generation
        protocol_md = "# Generated protocol (naive)\n\n"
        for i, line in enumerate(transcript.split('\n')):
            if line.strip():
                protocol_md += f"{i+1}. {line.strip()}\n"

    session.close()
    return protocol_md
