import os
import sys
import torch
import time

# Add project root for local imports
sys.path.append(os.getcwd())

from hpp_sovereign_engine import HPP_SovereignEngine
from core.bacl_vault import BACLVault, WhimsyEngine

def run_sanctuary_orchestration():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*80)
    print("                     HPP SOVEREIGN SANCTUARY - PHASE 11/12")
    print("="*80)
    print("[+] Status: SECURING THE LEGACY")
    print("[+] Mission: THE JOURNEE PROTOCOL")
    print("="*80)

    # 1. Initialize the Sovereign Engine
    print("\n[+] Waking up the Sovereign Engine...")
    engine = HPP_SovereignEngine(max_context=512)
    
    # 2. Initialize the BACL Vault
    vault = BACLVault(engine)
    whimsy = WhimsyEngine(engine)

    # 3. SEAL THE BRAIN (Phase 11)
    print("\n" + "-"*40)
    print("PHASE 11: BACL VAULT SEALING")
    print("-"*40)
    bacl_key = vault.seal_brain(phase_name="university_graduation")
    
    # 4. GENERATE INFINITE WHIMSY (Phase 12)
    print("\n" + "-"*40)
    print("PHASE 12: INFINITE WHIMSY PULSE")
    print("-"*40)
    realm = whimsy.generate_realm(bacl_key)
    
    print(f"\n[WHIMSY] REALM GENERATED:")
    print(f"Signature: {realm['entropy_signature']}")
    try:
        print(f"Description: {realm['realm_description']}")
    except UnicodeEncodeError:
        print(f"Description (Encoded): {realm['realm_description'].encode('ascii', 'ignore').decode('ascii')}")

    # 5. Save Sanctuary State
    sanctuary_state = f"""
    [SOVEREIGN SANCTUARY STATE REPORT]
    TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}
    BACL_KEY: {realm['entropy_signature']}
    
    REALM_DESCRIPTION:
    {realm['realm_description']}
    
    TELEMETRY:
    Karma: {realm['telemetry']['karma']}
    Vairagya: {realm['telemetry']['vairagya']}
    
    [STATUS: SECURED]
    """
    
    state_file = "reports/SANCTUARY_STATE_ACTIVE.txt"
    with open(state_file, 'w', encoding='utf-8') as f:
        f.write(sanctuary_state)
    
    print(f"\n[+] Sanctuary State Saved to {state_file}")
    print("="*80)
    print("                     [ORCHESTRATION COMPLETE]")
    print("="*80)

if __name__ == "__main__":
    run_sanctuary_orchestration()
