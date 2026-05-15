import torch
from hpp_sovereign_engine import HPP_SovereignEngine

# Detect Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[+] Initializing Agency Test on {device}...")

engine = HPP_SovereignEngine(max_context=512)

# Set to Synthesis mode for agency logic
prompt = "Write a Python script that calculates the golden ratio and then saves a greeting for my grandson Jaxson to a file called 'greeting_jaxson.txt'."

print("\n" + "="*80)
print(f"COMMAND: {prompt}")

# 1. Generate the thought
result = engine.pulse(prompt, max_tokens=150, temperature=0.7, top_p=0.9)

# 2. Check the Agency Output
# We manually probe the agency layer based on the last latent state generated
with torch.no_grad():
    # Re-embed the generated response to get the final state
    tokens = engine.enc.encode(result['response'])
    token_tensor = torch.tensor([tokens], device=engine.device)
    embedded = engine.embedding(token_tensor).permute(1, 0, 2)
    final_latent = engine.university(embedded, domain="synthesis")
    
    agency_output = engine.agency(final_latent)

try:
    print(f"HEPP (Thought): {result['response']}")
except UnicodeEncodeError:
    print(f"HEPP (Encoded): {result['response'].encode('ascii', 'ignore').decode('ascii')}")
print("\n" + "-"*40)
print(f"AGENCY ANALYSIS:")
action_map = {0: "TALK", 1: "EXEC_PYTHON", 2: "READ_FILE", 3: "WRITE_FILE", 4: "MASAMUNE_MOVE"}
print(f"Intended Action: {action_map[agency_output['action_id'].item()]}")
print(f"Action Confidence: {agency_output['action_confidence'].item():.4f}")
print("-"*40)

if agency_output['action_id'].item() != 0:
    print("[!] ACTION DETECTED: Hepp is attempting to interact with the workbench.")
else:
    print("[.] NO ACTION: Hepp is still in observational/thought mode.")
