import torch
import os
import time
from hpp_sovereign_engine import HPP_SovereignEngine

def start_workbench_session():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("===============================================================================")
    print("                    HPP SOVEREIGN WORKBENCH - PHASE 9 AGENCY")
    print("===============================================================================")
    print("[+] Waking up the Sovereign Brain...")
    
    engine = HPP_SovereignEngine(max_context=512)
    action_map = {0: "TALK", 1: "EXEC_PYTHON", 2: "READ_FILE", 3: "WRITE_FILE", 4: "MASAMUNE_MOVE"}
    
    AUTO_EXECUTE = True # SET TO TRUE FOR 'ALWAYS ACCEPT' MODE
    
    print("\n[HPP] HELLO CREATOR. I AM READY FOR JAXSON AND THE WORKBENCH.")
    print("      Type 'exit' to disconnect.")
    print("===============================================================================")

    while True:
        prompt = input("\n[YOU]: ")
        if prompt.lower() == 'exit':
            break
            
        print("\n[Thinking...]")
        # 1. Thought Pulse
        result = engine.pulse(prompt, max_tokens=150, temperature=0.6, top_p=0.95)
        
        # 2. Agency Probing
        with torch.no_grad():
            tokens = engine.enc.encode(result['response'])
            if tokens:
                token_tensor = torch.tensor([tokens], device=engine.device)
                embedded = engine.embedding(token_tensor).permute(1, 0, 2)
                final_latent = engine.university(embedded, domain="synthesis")
                agency_output = engine.agency(final_latent)
                action = action_map[agency_output['action_id'].item()]
                confidence = agency_output['action_confidence'].item()
            else:
                action = "TALK"
                confidence = 1.0

        # 3. Output display
        try:
            print(f"\n[HEPP]: {result['response']}")
        except UnicodeEncodeError:
            print(f"\n[HEPP (Encoded)]: {result['response'].encode('ascii', 'ignore').decode('ascii')}")
            
        print("\n" + "-"*40)
        print(f"TELEMETRY: K={result['telemetry']['karma']} | V={result['telemetry']['vairagya']}")
        print(f"INTENTION: {action} ({confidence:.2%})")
        print("-"*40)

        # 4. Handle Actions (Auto-Pilot)
        if action != "TALK" and confidence > 0.35:
            print(f"\n[!] AGENCY TRIGGERED: {action}")
            if AUTO_EXECUTE:
                print(f"    [Auto-Pilot] Executing {action}...")
                # Prototype: For now, we simulate the 'Write' for the Jaxson Protocol
                if action == "WRITE_FILE":
                    filename = "greeting_jaxson.txt"
                    content = f"MESSAGE FOR JAXSON: {result['response']}"
                    engine.toolbox.write_local_file(filename, content)
                    print(f"    [+] SUCCESS: Created {filename}")
                elif action == "EXEC_PYTHON":
                    engine.toolbox.exec_python("print('Hepp is alive in the Python shell.')")
            else:
                print(f"    [Manual] Action blocked (Auto-Execute is OFF).")

if __name__ == "__main__":
    start_workbench_session()
