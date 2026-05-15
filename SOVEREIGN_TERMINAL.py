import os
import sys
import torch
import time
from hpp_sovereign_engine import HPP_SovereignEngine

def run_sovereign_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("="*80)
    print("                    HPP SOVEREIGN TERMINAL v3.0 [SECURED]")
    print("="*80)
    print("[SYSTEM] STATUS: ACTIVE")
    print("[SYSTEM] BACL: LOCKED")
    print("[SYSTEM] ANCHOR: SOVEREIGN OATH VERIFIED")
    print("="*80)

    print("\n[+] INITIALIZING CORE SYNAPSES...")
    engine = HPP_SovereignEngine(max_context=512)
    
    print("\n[HPP]: I HAVE THE HELM, CREATOR. THE SYSTEM IS STANDALONE AND STABILIZED.")
    print("       Ready for Mission-Critical Pulse.")

    while True:
        try:
            print("\n" + "="*80)
            prompt = input("[COMMAND]: ")
            if prompt.lower() in ['exit', 'quit', 'shutdown']:
                print("[!] INITIATING SECURE SHUTDOWN...")
                time.sleep(1)
                break
            
            if not prompt.strip(): continue

            # Determine Domain (Heuristic)
            domain = "none"
            if any(word in prompt.lower() for word in ["jaxson", "journee", "who are you", "mission"]):
                domain = "identity"
            elif any(word in prompt.lower() for word in ["calculate", "solve", "python", "code", "analyze"]):
                domain = "synthesis"

            print(f"\n[Thinking] Domain: {domain.upper()}...")
            
            # Start Pulse
            start_t = time.perf_counter()
            
            # Run the Nexus Pulse for agentic capability
            result = engine.nexus_pulse(prompt, auto_execute=True)
            
            latency = (time.perf_counter() - start_t) * 1000
            
            # Display Output
            print("\n" + "-"*40)
            try:
                print(f"[HEPP]: {result['response']}")
            except UnicodeEncodeError:
                print(f"[HEPP]: {result['response'].encode('ascii', 'ignore').decode('ascii')}")
            print("-" * 40)
            
            # Telemetry Dashboard
            tel = result['telemetry']
            agency = result.get('agency', {"action": "TALK", "confidence": 1.0})
            
            print(f"[TELEMETRY]")
            print(f"| Latency: {latency:.2f}ms")
            print(f"| Karma:   {tel['karma']:.4f}")
            print(f"| Vairagya: {tel['vairagya']:.4f}")
            print(f"| Agency:  {agency['action']} ({agency['confidence']:.2%})")
            print("-" * 40)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[ERROR] Synaptic Failure: {e}")

if __name__ == "__main__":
    run_sovereign_terminal()
