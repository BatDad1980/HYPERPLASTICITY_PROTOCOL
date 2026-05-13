import os
import json
from datasets import load_dataset

def localize_advanced_curriculum():
    os.makedirs("datasets/hf_local", exist_ok=True)
    
    # 1. NATURAL INSTRUCTIONS (Task Generalization)
    print("Downloading Natural Instructions (V2)...")
    try:
        ds = load_dataset("Muennighoff/natural-instructions", split="train", streaming=True)
        save_path = "datasets/hf_local/GENERAL_TASK_FOLLOWING.jsonl"
        print(f"  Streaming and saving tasks...")
        with open(save_path, 'w', encoding='utf-8') as f:
            count = 0
            for sample in ds:
                # Muennighoff/natural-instructions format might vary, checking instruction/input/output
                # If it's a dict with 'text', use that. If it's 'instruction'/'input'/'output', combine.
                if 'instruction' in sample:
                    text = f"Instruction: {sample['instruction']}\nInput: {sample['input']}\nOutput: {sample['output']}"
                else:
                    text = sample.get('text', str(sample))
                f.write(json.dumps({"text": text}) + "\n")
                count += 1
                if count >= 1000: break
        print(f"  {count} NI tasks cached.")
    except Exception as e:
        print(f"  Failed Natural Instructions: {e}")

    # 2. S2ORC (Academic Reasoning)
    print("Downloading S2ORC (Academic Research)...")
    try:
        ds = load_dataset("sentence-transformers/s2orc", split="train", streaming=True)
        save_path = "datasets/hf_local/ACADEMIC_RESEARCH.jsonl"
        with open(save_path, 'w', encoding='utf-8') as f:
            count = 0
            for sample in ds:
                # sentence-transformers/s2orc usually has 'title', 'abstract'
                text = f"Title: {sample.get('title', 'N/A')}\nAbstract: {sample.get('abstract', 'N/A')}"
                f.write(json.dumps({"text": text}) + "\n")
                count += 1
                if count >= 1000: break
        print(f"  {count} S2ORC papers cached.")
    except Exception as e:
        print(f"  Failed S2ORC: {e}")

    # 3. WINOGRANDE (Commonsense Reasoning - Medium)
    print("Downloading Winogrande (Medium)...")
    try:
        ds = load_dataset("allenai/winogrande", "winogrande_m", split="train")
        save_path = "datasets/hf_local/COMMONSENSE_REASONING.jsonl"
        print(f"  Found {len(ds)} samples. Saving...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(min(2000, len(ds))):
                sample = ds[i]
                text = f"Sentence: {sample['sentence']}\nOption 1: {sample['option1']}\nOption 2: {sample['option2']}\nCorrect Option: {sample['answer']}"
                f.write(json.dumps({"text": text}) + "\n")
        print("  Winogrande cached.")
    except Exception as e:
        print(f"  Failed Winogrande: {e}")

    # 4. AIME (Olympiad Math)
    print("Downloading AIME 2025 (Elite Math)...")
    try:
        ds = load_dataset("math-ai/aime25", split="test")
        save_path = "datasets/hf_local/OLYMPIAD_MATH.jsonl"
        print(f"  Found {len(ds)} samples. Saving...")
        with open(save_path, 'w', encoding='utf-8') as f:
            for i in range(len(ds)):
                sample = ds[i]
                # math-ai/aime25 usually has 'problem' and 'solution' or 'answer'
                prob = sample.get('problem', sample.get('question', ''))
                sol = sample.get('solution', sample.get('answer', ''))
                text = f"Problem: {prob}\nSolution: {sol}"
                f.write(json.dumps({"text": text}) + "\n")
        print("  AIME cached.")
    except Exception as e:
        print(f"  Failed AIME: {e}")

if __name__ == "__main__":
    localize_advanced_curriculum()
