import os
import json
from datasets import load_dataset

def localize_adolescent_curriculum():
    os.makedirs("datasets/hf_local", exist_ok=True)
    
    curriculums = [
        {"name": "PHILOSOPHY", "subset": "philosophy"},
        {"name": "FORMAL_LOGIC", "subset": "formal_logic"},
        {"name": "MORAL_SCENARIOS", "subset": "moral_scenarios"},
        {"name": "WORLD_RELIGIONS", "subset": "world_religions"} # Abstract concepts
    ]
    
    for c in curriculums:
        print(f"Downloading {c['name']} (MMLU)...")
        try:
            # Using 'test' split for data volume
            ds = load_dataset("cais/mmlu", c['subset'], split="test")
            save_path = f"datasets/hf_local/{c['name']}.jsonl"
            print(f"  Found {len(ds)} samples. Saving...")
            with open(save_path, 'w', encoding='utf-8') as f:
                for i in range(len(ds)):
                    sample = ds[i]
                    # MMLU has 'question', 'choices', 'answer' (index)
                    question = sample['question']
                    choices = "\n".join([f"{chr(65+j)}) {choice}" for j, choice in enumerate(sample['choices'])])
                    answer = chr(65 + sample['answer'])
                    
                    text = f"Question: {question}\nChoices:\n{choices}\nCorrect Answer: {answer}"
                    f.write(json.dumps({"text": text}) + "\n")
            print(f"  {c['name']} cached.")
        except Exception as e:
            print(f"  Failed {c['name']}: {e}")

if __name__ == "__main__":
    localize_adolescent_curriculum()
