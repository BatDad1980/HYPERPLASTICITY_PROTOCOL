"""Safe V2 speech smoke test.

Inference only. This does not train or modify checkpoints.
"""
import sys
sys.path.append('.')
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2

e = HPP_SovereignEngine_V2(max_context=512)
e.set_power_mode("demo")
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
        r = e.pulse(
            q,
            max_tokens=48,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            ngram_block=3,
            frequency_penalty=1.25,
            presence_penalty=0.45,
            min_tokens=8,
        )
        print(f"Q: {q}", flush=True)
        print(f"A: {r['response'][:200]}", flush=True)
        print(f"tokens={r['tokens']} latency_ms={r['latency_ms']} domain={r.get('domain_used')}", flush=True)
        print(flush=True)
    except Exception as ex:
        print(f"Q: {q}", flush=True)
        print(f"[ERROR] {ex}", flush=True)
        print(flush=True)
