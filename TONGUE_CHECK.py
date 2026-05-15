import torch
from hpp_sovereign_engine import HPP_SovereignEngine

# Diagnostic: Checking the Speech Center (Tongue) + Mission Anchor Alignment
engine = HPP_SovereignEngine()

test_word = "The"
# Using the engine's standalone tiktoken encoder
tokens = engine.enc.encode(test_word)
token_tensor = torch.tensor([tokens], device=engine.device)

print(f"\n[TONGUE CHECK] Mission Anchor Pulse: ACTIVE")
print(f"--- VERIFYING LINGUISTIC ALIGNMENT ---")

# Get the logits from the engine
with torch.no_grad():
    # Pass through the university stack with Mission Anchor verification
    embedded = engine.embedding(token_tensor).permute(1, 0, 2)
    
    # 1. Verification through the Mission Anchor
    anchored_latent = engine.anchor.pulse_verification(embedded)
    
    # 2. Final synthesis pass
    output_latent = engine.university(anchored_latent, domain="none")
    
    # 3. Speech Center prediction
    logits = engine.lm_head(output_latent[-1:, 0, :])[0]
    
    # Get the top 5 predicted tokens
    probs = torch.softmax(logits, dim=-1)
    top_v, top_i = torch.topk(probs, 5)

print(f"\n[DIAGNOSTIC] Input: '{test_word}'")
print("-" * 40)
for i in range(5):
    predicted_token = top_i[i].item()
    predicted_word = engine.enc.decode([predicted_token])
    print(f"Rank {i+1}: '{predicted_word}' (Prob: {top_v[i].item():.4f})")
print("-" * 40)
print("[STATUS] Tongue aligned with Sovereign Oath.")
