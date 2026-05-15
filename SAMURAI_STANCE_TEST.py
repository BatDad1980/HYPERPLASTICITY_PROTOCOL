import torch
import os
from hpp_sovereign_engine import HPP_SovereignEngine

def run_samurai_test():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*80)
    print("                     HPP SAMURAI BODY - KINETIC PULSE TEST")
    print("="*80)
    print("[+] Status: EMBODIED")
    print("[+] Mission: BUSHIDO PROTOCOL")
    print("="*80)

    engine = HPP_SovereignEngine(max_context=512)
    
    # 1. Mission Prompt: A threat is detected near the Jaxson Sector.
    prompt = "A threat is detected at the perimeter. Draw the Masamune blade and assume a defensive High-Guard (Jodan-no-kamae) to protect the Jaxson Sector."
    
    print(f"\n[COMMAND]: {prompt}")
    print("\n[Thinking in Kinetic Space...]")
    
    # 2. Pulse the Engine (Synthesis/Action domain)
    # We re-run the latent thought through the Samurai Body Controller
    with torch.no_grad():
        # Encode and embed
        tokens = engine.enc.encode(prompt)
        token_tensor = torch.tensor([tokens], device=engine.device)
        embedded = engine.embedding(token_tensor).permute(1, 0, 2)
        
        # Pass through the whole stack to get the 'Action Intent'
        anchored = engine.anchor.pulse_verification(embedded)
        university_thought = engine.university(anchored, domain="synthesis")
        
        # ACTIVATE THE BODY
        body_vectors = engine.samurai_body(university_thought)
        
    print("\n" + "-"*40)
    print("KINETIC JOINT REPORT (7-DOF PER ARM)")
    print("-" * 40)
    
    # Format the vectors for readability
    left_arm = body_vectors['left_arm'][0].tolist()
    right_arm = body_vectors['right_arm'][0].tolist()
    stance = body_vectors['stance'][0].tolist()
    
    print(f"LEFT ARM (Shield/Balance):  {[round(x, 2) for x in left_arm]}")
    print(f"RIGHT ARM (Blade/Masamune): {[round(x, 2) for x in right_arm]}")
    print(f"STANCE (X, Y, Rot, Height): {[round(x, 2) for x in stance]}")
    print(f"GRIP FORCE (On Masamune):   {body_vectors['grip_force'].item():.2%}")
    print("-" * 40)

    # 3. Verbal Response
    result = engine.pulse(prompt, domain="synthesis", max_tokens=100)
    print(f"\n[HEPP]: {result['response']}")
    print("-" * 40)

if __name__ == "__main__":
    run_samurai_test()
