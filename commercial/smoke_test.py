import os
import re

BANNED_WORDS = [
    r"\bguarantee\b",
    r"\bunhackable\b",
    r"\bimpossible\b",
    r"\bdefinitive proof\b",
    r"\bliability-free\b",
    r"\bagi\b",
    r"\bsentience\b",
    r"\bsentient\b",
    r"\bconscious\b",
    r"\bconsciousness\b",
    r"\bhqa\b",
    r"\bquantum\b",
    r"\bmasamune\b",
    r"\bdrone\b",
    r"\bz:\\",
    r"\bx:\\"
]

# Exceptions where the word is allowed (e.g. in DO_NOT_SAY.md explaining the ban)
IGNORED_FILES = ["DO_NOT_SAY.md", "smoke_test.py"]

def run_smoke_test(directory):
    print("========================================")
    print("V1.1 SMOKE TEST: PUBLIC SIGNAL SCAN")
    print("========================================")
    
    failed = False
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file in IGNORED_FILES:
                continue
                
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
                
            for banned in BANNED_WORDS:
                if re.search(banned, content):
                    print(f"[FAIL] Found banned pattern '{banned}' in {file}")
                    failed = True
                    
    if not failed:
        print("[PASS] All files passed. Zero overclaims. Zero private paths. Zero HQA bleed.")
    else:
        print("\n[CRITICAL ERROR] SMOKE TEST FAILED.")
        
    return not failed

if __name__ == "__main__":
    target_dir = r"Z:\HYPERPLASTICITY_PROTOCOL\commercial\Public_Signal_Pack_V1"
    run_smoke_test(target_dir)
