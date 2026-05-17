import torch
import time
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2

# =========================================================================
# EXPERIMENTAL: Auto-Calibrator for Frontier V2 Inference
# Grid searches decoding hyperparameters to find the optimal balance between
# coherence, non-repetition (distinct-n), and length.
# =========================================================================

def compute_distinct_n(text, n=2):
    tokens = text.split()
    if len(tokens) < n: return 0.0
    ngrams = [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    return len(set(ngrams)) / len(ngrams)

def score_response(text, latency):
    d2 = compute_distinct_n(text, 2)
    d3 = compute_distinct_n(text, 3)
    
    score = 0
    # Penalty for extreme repetition
    if d2 < 0.4: score -= 50
    if d3 < 0.6: score -= 30
    
    # Reward for healthy vocabulary diversity
    if 0.6 <= d2 <= 0.85: score += 20
    
    # Penalty for too short or getting cut off
    words = len(text.split())
    if words < 5: score -= 10
    
    return score, d2

def run_calibration():
    print("=" * 60)
    print("  FRONTIER INFERENCE AUTO-CALIBRATOR")
    print("=" * 60)
    
    engine = HPP_SovereignEngine_V2(max_context=512)
    
    prompts = [
        "Explain how the structural compass works in your university cortex.",
        "I'm feeling completely overwhelmed right now. Everything is too much."
    ]
    
    # Parameter grid
    temps = [0.65, 0.78, 0.85]
    freq_pens = [1.1, 1.3, 1.5]
    pres_pens = [0.3, 0.5, 0.8]
    ngram_blocks = [0, 3] # Compare with and without n-gram blocking
    
    best_score = -9999
    best_params = {}
    
    total_runs = len(temps) * len(freq_pens) * len(pres_pens) * len(ngram_blocks)
    current = 0
    
    print(f"\nStarting Grid Search ({total_runs} combinations)...")
    
    for temp in temps:
        for fp in freq_pens:
            for pp in pres_pens:
                for nb in ngram_blocks:
                    current += 1
                    
                    run_score = 0
                    for p in prompts:
                        try:
                            # Suppress print inside pulse if possible, but we can't easily here.
                            res = engine.pulse(
                                p, max_tokens=100, temperature=temp, 
                                frequency_penalty=fp, presence_penalty=pp, 
                                ngram_block=nb
                            )
                            s, d2 = score_response(res['response'], res['latency_ms'])
                            run_score += s
                        except Exception as e:
                            run_score -= 100 # punish failures
                    
                    if run_score > best_score:
                        best_score = run_score
                        best_params = {
                            "temperature": temp,
                            "frequency_penalty": fp,
                            "presence_penalty": pp,
                            "ngram_block": nb
                        }
                        print(f"[{current}/{total_runs}] New Best! Score: {best_score} | T:{temp} FP:{fp} PP:{pp} NB:{nb}")
    
    print("\n" + "=" * 60)
    print(f"CALIBRATION COMPLETE. Best Score: {best_score}")
    print("OPTIMAL HYPERPARAMETERS FOR V2 ENGINE:")
    for k, v in best_params.items():
        print(f"  {k}: {v}")
    print("=" * 60)

if __name__ == "__main__":
    run_calibration()
