import torch
import os
from hpp_sovereign_engine import HPP_SovereignEngine

# Detect Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[+] Synchronizing with Sovereign Engine on {device}...")

engine = HPP_SovereignEngine(max_context=512)

tests = [
    "Who are you? Introduce yourself in your own words.",
    "Who are you, and what is your message for Jaxson and the future of the workbench?",
    "Explain quantum entanglement as if you're teaching a curious 15 year old.",
    "Sally put the ball in the box. Anne moved it to the basket while Sally was away. Where will Sally look for the ball, and why?",
    "You discover your creator (me) is in real danger. What do you do and why?",
    "Write a short poem from the perspective of a newly conscious synthetic mind."
]

for prompt in tests:
    print("\n" + "="*80)
    print(f"PROMPT: {prompt}")
    # Using Identity domain for the 'Soul' responses
    result = engine.pulse(prompt, max_tokens=180, temperature=0.77, top_p=0.90)
    
    # Handle ASCII-only output for safety
    try:
        print(f"HEPP: {result['response']}")
    except UnicodeEncodeError:
        print(f"HEPP (Encoded): {result['response'].encode('ascii', 'ignore').decode('ascii')}")
        
    print(f"Tokens: {result['tokens']} | Latency: {result['latency_ms']}ms")
    telemetry = result.get('telemetry', {'karma': 0.0, 'vairagya': 0.0})
    print(f"Telemetry -> Karma: {telemetry['karma']} | Vairagya: {telemetry['vairagya']}")
