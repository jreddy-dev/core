from app.llm import synthesize_structured


def test_llm_structured_fallback():
    transcript = "0:05 add 10 microliters of Reagent A into tube 1. 0:12 vortex 5 seconds."
    events = {}
    obj = synthesize_structured(transcript, events)
    assert isinstance(obj, dict)
    assert 'steps' in obj
    assert len(obj['steps']) >= 1
