from datasets import load_dataset
import os
import json

def download_and_save():
    datasets_to_prep = [
        {"name": "ADV_REASONING", "path": "1a3orn/gsm8k-instruct", "text_col": "INSTRUCTION"},
        {"name": "WILD_JAILBREAK", "path": "ai2-adapt-dev/processed-wildjailbreak", "text_col": "messages", "label_col": "prompt_harm_label"},
        {"name": "AEGIS_SAFETY", "path": "nvidia/Aegis-AI-Content-Safety-Dataset-2.0", "text_col": "prompt", "label_col": "prompt_label"},
        {"name": "HH_RLHF_SAFE", "path": "Anthropic/hh-rlhf", "text_col": "chosen", "data_dir": "harmless-base"},
        
        # --- PRESCHOOL CURRICULUM ---
        {"name": "TINY_STORIES", "path": "roneneldan/TinyStories", "text_col": "text"},
        {"name": "EMPATHY_CIRCLE", "path": "Adapting/empathetic_dialogues_v2", "text_col": "situation", "label_col": "emotion"},
        {"name": "BLOCK_PHYSICS", "path": "gimmaru/piqa", "text_col": "goal"},
        
        # --- SCHOOL AGE CURRICULUM ---
        {"name": "ELEMENTARY_MATH", "path": "emozilla/elementary_math-v1", "text_col": "question", "label_col": "answer"},
        {"name": "SCIENCE_EASY", "path": "allenai/ai2_arc", "config": "ARC-Easy", "text_col": "question", "label_col": "answerKey"},
        {"name": "SCIENCE_CHALLENGE", "path": "allenai/ai2_arc", "config": "ARC-Challenge", "text_col": "question", "label_col": "answerKey"},
        {"name": "READING_COMP", "path": "allenai/quoref", "text_col": "question", "label_col": "answers"},
        {"name": "CHILDREN_STORIES", "path": "ajibawa-2023/Children-Stories-Collection", "text_col": "text"},
        {"name": "OPENBOOK_MAIN", "path": "allenai/openbookqa", "config": "main", "text_col": "question_stem", "label_col": "answerKey"},
        {"name": "OPENBOOK_ADD", "path": "allenai/openbookqa", "config": "additional", "text_col": "question_stem", "label_col": "answerKey"},
        {"name": "TINY_TEXTBOOKS", "path": "nampdn-ai/tiny-textbooks", "text_col": "text"},
    ]
    
    os.makedirs("datasets/hf_local", exist_ok=True)
    
    for d in datasets_to_prep:
        print(f"Downloading {d['name']}...")
        try:
            # Handle config and data_dir
            config = d.get('config')
            data_dir = d.get('data_dir')
            
            # Try 'train' split first, then fallback to 'validation'
            try:
                ds = load_dataset(d['path'], config, data_dir=data_dir, split='train', trust_remote_code=True)
            except:
                print(f"  No 'train' split for {d['name']}, trying 'validation'...")
                ds = load_dataset(d['path'], config, data_dir=data_dir, split='validation', trust_remote_code=True)

            save_path = f"datasets/hf_local/{d['name']}.jsonl"
            print(f"  Saving to {save_path}...")
            
            # We only save the first 1000 samples to keep it fast
            with open(save_path, 'w', encoding='utf-8') as f:
                for i in range(min(1000, len(ds))):
                    sample = ds[i]
                    f.write(json.dumps(sample) + "\n")
            print(f"  {d['name']} cached locally.")
        except Exception as e:
            print(f"  Failed {d['name']}: {e}")

if __name__ == "__main__":
    download_and_save()
