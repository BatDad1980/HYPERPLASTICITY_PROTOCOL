import os
import json
import pandas as pd
from datasets import load_dataset
import urllib.request

def localize_new_curriculum():
    os.makedirs("datasets/hf_local", exist_ok=True)
    
    # 1. BEAVERTAILS (Safety & Alignment)
    print("Downloading BeaverTails (Safety)...")
    try:
        ds = load_dataset("PKU-Alignment/BeaverTails", split="30k_train")
        save_path = "datasets/hf_local/ETHICAL_HARDENING.jsonl"
        print(f"  Found {len(ds)} samples. Saving to {save_path}...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(min(2000, len(ds))):
                sample = ds[i]
                f.write(json.dumps({
                    "instruction": sample['prompt'],
                    "response": sample['response'],
                    "is_safe": sample['is_safe']
                }) + "\n")
        print("  BeaverTails cached.")
    except Exception as e:
        print(f"  Failed BeaverTails: {e}")

    # 2. ToM-QA (Theory of Mind)
    print("Downloading ToM-QA (Social Cognition)...")
    try:
        ds = load_dataset("grimulkan/theory-of-mind", split="train")
        save_path = "datasets/hf_local/SOCIAL_COG.jsonl"
        print(f"  Found {len(ds)} samples. Saving to {save_path}...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(len(ds)):
                sample = ds[i]
                # Combine instruction, input, and response for training
                text = f"{sample['instruction']}\n{sample['input']}\n{sample['response']}"
                f.write(json.dumps({
                    "text": text,
                }) + "\n")
        print("  ToM-QA cached.")
    except Exception as e:
        print(f"  Failed ToM-QA: {e}")

    # 3. SENSE-7 (Empathy)
    print("Downloading SENSE-7 (Structured Empathy)...")
    sense_url = "https://raw.githubusercontent.com/microsoft/sense-7/main/sense-7_dataset.xlsx"
    try:
        local_xlsx = "datasets/sense-7_dataset.xlsx"
        print(f"  Downloading Excel from {sense_url}...")
        urllib.request.urlretrieve(sense_url, local_xlsx)
        
        print(f"  Converting Excel to JSONL...")
        df = pd.read_excel(local_xlsx, sheet_name="Messages")
        save_path = "datasets/hf_local/HIGH_FIDELITY_EMPATHY.jsonl"
        with open(save_path, 'w', encoding='utf-8') as f:
            for _, row in df.iterrows():
                f.write(json.dumps({
                    "role": row['Role'],
                    "text": str(row['Content']),
                    "empathy_score": row['EmpathyOverall']
                }) + "\n")
        print("  SENSE-7 cached.")
    except Exception as e:
        print(f"  Failed SENSE-7: {e}")

if __name__ == "__main__":
    localize_new_curriculum()
