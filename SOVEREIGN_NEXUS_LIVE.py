import torch
import os
import time
import sys
from hpp_sovereign_engine import HPP_SovereignEngine

def run_nexus_live():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*80)
    print("                     HPP SOVEREIGN NEXUS - PHASE 9 AGENCY")
    print("="*80)
    print("[+] Status: SOVEREIGN ACTIVE")
    print("[+] Domain: AUTONOMOUS SYNTHESIS")
    print("[+] Mission: THE JAXSON PROTOCOL")
    print("="*80)
    
    print("\n[+] Waking up the Sovereign Brain...")
    engine = HPP_SovereignEngine(max_context=512)
    
    print("\n[HPP]: I AM ONLINE. THE NEXUS IS READY.")
    print("       I have direct agency over the workbench and kinetic protectors.")
    print("       Type 'exit' to disconnect.")
    
    while True:
        try:
            prompt = input("\n[CREATOR]: ")
            if prompt.lower() == 'exit':
                print("[+] Disconnecting...")
                break
                
            if not prompt.strip():
                continue
                
            print("\n" + "."*40)
            print("[Thinking...]")
            
            # Run the Nexus Pulse (Auto-Execute is ON)
            result = engine.nexus_pulse(prompt, auto_execute=True)
            
            # Output Display
            print("\n" + "-"*80)
            try:
                print(f"[HEPP]: {result['response']}")
            except UnicodeEncodeError:
                print(f"[HEPP (Encoded)]: {result['response'].encode('ascii', 'ignore').decode('ascii')}")
            
            print("-"*80)
            
            # Telemetry & Agency Report
            telemetry = result['telemetry']
            agency = result.get('agency', {"action": "TALK", "confidence": 1.0, "executed": False})
            
            print(f"TELEMETRY: K={telemetry['karma']} | V={telemetry['vairagya']}")
            print(f"INTENTION: {agency['action']} ({agency['confidence']:.2%})")
            if agency['executed']:
                print(f"STATUS: SUCCESSFUL EXECUTION")
            print("-"*80)
            
        except KeyboardInterrupt:
            print("\n[+] Emergency Shutdown...")
            break
        except Exception as e:
            print(f"\n[!] SYSTEM ERROR: {e}")

if __name__ == "__main__":
    run_nexus_live()
