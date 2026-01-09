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
    events = {}
    if pr and pr.transcripts:
        for s in pr.transcripts.get("segments", []):
            transcript += s.get("text", "") + "\n"
    if pr:
        events = {"actions": pr.actions or [], "detections": pr.detections or {}, "ocr": pr.ocr or {}}

    # structured synthesis via llm helper
    try:
        from . import llm
        structured = llm.synthesize_structured(transcript, events)
        # render markdown summary for backward compatibility
        md = "# Generated protocol (structured)\n\n"
        for st in structured.get('steps', []):
            md += f"{st.get('step_number')}. {st.get('action')}\n"
        session.close()
        return md
    except Exception:
        # fallback to older method
        session.close()
        return "# Generated protocol (naive)\n\n" + transcript[:1000]


def synthesize_structured(video_id: str):
    session = SessionLocal()
    pr = session.query(ProcessingResult).filter(ProcessingResult.video_id == video_id).order_by(ProcessingResult.created_at.desc()).first()
    transcript = ""
    events = {}
    if pr and pr.transcripts:
        for s in pr.transcripts.get("segments", []):
            transcript += s.get("text", "") + "\n"
    if pr:
        events = {"actions": pr.actions or [], "detections": pr.detections or {}, "ocr": pr.ocr or {}}
    try:
        from . import llm
        return llm.synthesize_structured(transcript, events)
    except Exception:
        return {"steps": [], "reagents": [], "equipment": [], "assumptions": []}
