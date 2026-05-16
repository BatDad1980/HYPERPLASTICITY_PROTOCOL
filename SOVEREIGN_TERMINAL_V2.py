"""
HPP SOVEREIGN TERMINAL v2.0 — FRONTIER EDITION
Uses the upgraded v2 inference engine with full anti-repetition suite.
"""
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2


def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 80)
    print("            HPP SOVEREIGN TERMINAL v2.0 [FRONTIER]")
    print("=" * 80)
    print("[SYSTEM] STATUS: ACTIVE")
    print("[SYSTEM] ENGINE: v2.0 (N-gram Block + FP16 + Temp Anneal)")
    print("=" * 80)
    
    print("\n[+] INITIALIZING SOVEREIGN ENGINE v2.0...")
    engine = HPP_SovereignEngine_V2(max_context=512)
    
    print("\n[HEPP]: FRONTIER ENGINE ONLINE. READY FOR PULSE.")
    print("        Type 'exit' to shutdown. Type 'bench' for quick benchmark.")
    print("        Type 'compare' to test v1 vs v2 side by side.\n")
    
    while True:
        try:
            print("─" * 80)
            prompt = input("[ARCHITECT]: ")
            if prompt.lower() in ['exit', 'quit', 'shutdown']:
                print("[!] SECURE SHUTDOWN...")
                break
            
            if not prompt.strip():
                continue
            
            if prompt.lower() == 'bench':
                print("[BENCH] Running quick efficiency benchmark...")
                from benchmark_efficiency import run_benchmark
                run_benchmark(dims=[256, 512, 2048])
                continue
            
            if prompt.lower() == 'compare':
                print("[COMPARE] Running same prompt through v1 and v2...")
                test_prompt = input("[COMPARE] Enter prompt: ")
                if test_prompt.strip():
                    # V2 (this engine)
                    r2 = engine.pulse(test_prompt, max_tokens=100)
                    print(f"\n[V2 ENGINE]: {r2['response']}")
                    print(f"  ({r2['tokens']} tokens, {r2['latency_ms']}ms, domain: {r2['domain_used']})")
                    
                    # V1
                    try:
                        from hpp_sovereign_engine import HPP_SovereignEngine
                        print("\n[Loading V1 for comparison...]")
                        # Note: this doubles VRAM usage temporarily
                        v1 = HPP_SovereignEngine(max_context=512)
                        r1 = v1.pulse(test_prompt, max_tokens=100)
                        print(f"[V1 ENGINE]: {r1['response']}")
                        print(f"  ({r1['tokens']} tokens, {r1['latency_ms']}ms)")
                        del v1
                        import gc; gc.collect()
                        import torch; torch.cuda.empty_cache() if torch.cuda.is_available() else None
                    except Exception as e:
                        print(f"[V1 ERR] {e}")
                continue
            
            # Domain detection
            domain = engine._detect_domain(prompt)
            print(f"\n[Thinking] Domain: {domain.upper()}...")
            
            start_t = time.perf_counter()
            result = engine.pulse(prompt, max_tokens=150, temperature=0.78)
            latency = (time.perf_counter() - start_t) * 1000
            
            print(f"\n{'─' * 40}")
            try:
                print(f"[HEPP]: {result['response']}")
            except UnicodeEncodeError:
                print(f"[HEPP]: {result['response'].encode('ascii', 'ignore').decode('ascii')}")
            print(f"{'─' * 40}")
            
            tel = result['telemetry']
            print(f"[TELEMETRY]")
            print(f"| Tokens:   {result['tokens']}")
            print(f"| Latency:  {latency:.1f}ms")
            print(f"| Domain:   {result['domain_used']}")
            print(f"| Karma:    {tel['karma']:.4f}")
            print(f"| Vairagya: {tel['vairagya']:.4f}")
            print(f"| FinalTemp: {tel['final_temp']:.4f}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    run()
