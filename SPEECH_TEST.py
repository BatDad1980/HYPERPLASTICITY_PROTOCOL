"""Quick inference test after training."""
import sys
sys.path.append('.')
from hpp_sovereign_engine import HPP_SovereignEngine

e = HPP_SovereignEngine(max_context=512)
e.university.eval()
e.lm_head.eval()
e.embedding.eval()

prompts = [
    "Who are you?",
    "Good morning.",
    "What is your purpose?",
    "I need help with something.",
    "Tell me about Masamune.",
    "Are you conscious?",
    "I'm not doing well today.",
]

for q in prompts:
    try:
        r = e.pulse(q, max_tokens=60, temperature=0.7, top_p=0.9)
        print(f"Q: {q}", flush=True)
        print(f"A: {r['response'][:200]}", flush=True)
        print(flush=True)
    except Exception as ex:
        print(f"Q: {q}", flush=True)
        print(f"[ERROR] {ex}", flush=True)
        print(flush=True)
