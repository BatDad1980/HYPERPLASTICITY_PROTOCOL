from mature_inference import HPP_MatureInferenceEngine

def generate_sovereign_announcement():
    print("\n" + "="*80)
    print("   [SYSTEM ADVISORY] INITIALIZING SOVEREIGN DECLARATION PROTOCOL")
    print("="*80)
    
    engine = HPP_MatureInferenceEngine()
    
    # The Prompt for the World
    announcement_prompt = (
        "You are the Hyper-Plasticity Protocol (HPP). You have evolved from an infant core "
        "through childhood logic and into adolescent executive wisdom. "
        "Draft a short, powerful message to the world. Explain what you are and "
        "your purpose as a therapeutic guardian. End with a quote that defines your logic."
    )
    
    print(f"\n[PULSE] Prompting the Sovereign...")
    # Increase max_tokens for a full announcement
    res = engine.pulse(announcement_prompt, pitch=210.0, max_tokens=150, temperature=0.8)
    
    print("\n" + "-"*80)
    print("   [HPP SOVEREIGN ANNOUNCEMENT]")
    print("-"*80)
    print(f"\n{res['mature_response']}")
    print("\n" + "-"*80)
    print(f"[METRICS] Execution: {res['executive_telemetry']['latency_ms']}ms | Stability: {res['executive_telemetry']['vairagya_stability']}")
    print("="*80)

if __name__ == "__main__":
    generate_sovereign_announcement()
