import os
import json
from datasets import load_dataset

def localize_logic_lens():
    os.makedirs("datasets/hf_local", exist_ok=True)
    
    # 1. COT LOGIC REASONING (Chain-of-Thought)
    print("Downloading CoT Logic Reasoning...")
    try:
        # isaiahbjork/cot-logic-reasoning
        ds = load_dataset("isaiahbjork/cot-logic-reasoning", split="train")
        save_path = "datasets/hf_local/LOGIC_LENS.jsonl"
        print(f"  Found {len(ds)} samples. Saving...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(min(5000, len(ds))):
                sample = ds[i]
                # Combine instruction and reasoning into a single string for Hepp
                text = f"Instruction: {sample.get('instruction', '')}\nReasoning: {sample.get('thought', '')}\nConclusion: {sample.get('output', '')}"
                f.write(json.dumps({"text": text}) + "\n")
        print("  Logic Lens cached.")
    except Exception as e:
        print(f"  Failed CoT Logic: {e}")

    # 2. LOGICAL FALLACY (Specific examples)
    print("Downloading Logical Fallacy dataset...")
    try:
        ds = load_dataset("tasksource/logical-fallacy", split="train")
        save_path = "datasets/hf_local/LOGICAL_FALLACIES.jsonl"
        print(f"  Found {len(ds)} samples. Saving...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(min(2000, len(ds))):
                sample = ds[i]
                text = f"Statement: {sample['text']}\nFallacy: {sample['label']}\nExplanation: {sample.get('explanation', 'N/A')}"
                f.write(json.dumps({"text": text}) + "\n")
        print("  Logical Fallacies cached.")
    except Exception as e:
        print(f"  Failed Logical Fallacy: {e}")

if __name__ == "__main__":
    localize_logic_lens()
