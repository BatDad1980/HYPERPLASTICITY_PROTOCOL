import json
import os
import random

# Procedural Augmentation Script for HPP
# Takes the existing CONVERSATIONAL_FLUENCY.jsonl and explodes it by applying
# various conversational wrappers (greetings, acknowledgments, tonal shifts).

def load_data(filepath):
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(json.loads(line))
    return data

def save_data(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            if 'text' not in item:
                item['text'] = f"### Instruction:\n{item['instruction']}\n\n### Response:\n{item['response']}"
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# Augmentation templates
PREFIXES = [
    "Hey Hepp, ", "Question for you: ", "Tell me, ", "Can you explain: ",
    "I was wondering, ", "Quick question: ", "Hepp, ", "Okay, next thing: ",
    "Listen, ", "Hey buddy, ", "Architect here. ", "System check: "
]

SUFFIXES = [
    " Make it quick.", " Explain it simply.", " What are your thoughts?",
    " Any ideas?", " Let me know.", " What's the status?",
    " Do you agree?", " Give me the details."
]

RESP_PREFIXES = [
    "Acknowledged. ", "Understood. ", "Here is the information: ", "Of course. ",
    "Let's look at this. ", "Processing... ", "I can help with that. ", "Affirmative. ",
    "Interesting. ", "Alright. ", "As requested: ", "Here is what I know: "
]

def augment_sample(sample):
    new_samples = []
    inst = sample['instruction'].strip()
    resp = sample['response'].strip()
    cat = sample.get('category', 'conversation')
    
    # Strategy 1: Add prefix to instruction
    p = random.choice(PREFIXES)
    new_inst = f"{p}{inst[0].lower()}{inst[1:]}" if inst[0].isupper() else f"{p}{inst}"
    new_samples.append({"instruction": new_inst, "response": resp, "category": cat})
    
    # Strategy 2: Add suffix to instruction, prefix to response
    s = random.choice(SUFFIXES)
    r = random.choice(RESP_PREFIXES)
    new_inst2 = f"{inst}{s}"
    new_resp2 = f"{r}{resp[0].lower()}{resp[1:]}" if resp[0].isupper() and not resp.startswith("I ") else f"{r}{resp}"
    new_samples.append({"instruction": new_inst2, "response": new_resp2, "category": cat})
    
    # Strategy 3: Both (for robustness)
    new_samples.append({"instruction": f"{p}{inst}{s}", "response": f"{r}{resp}", "category": cat})
    
    return new_samples

def main():
    base_path = "datasets/hf_local/CONVERSATIONAL_FLUENCY.jsonl"
    out_path = "datasets/hf_local/CONVERSATIONAL_FLUENCY_AUGMENTED.jsonl"
    
    print("Loading base dataset...")
    base_data = load_data(base_path)
    print(f"Base size: {len(base_data)}")
    
    augmented_data = list(base_data)  # keep originals
    
    for sample in base_data:
        # Generate 3 variations per sample
        variations = augment_sample(sample)
        augmented_data.extend(variations)
    
    # Remove duplicates based on exact instruction match just in case
    seen = set()
    final_data = []
    for s in augmented_data:
        key = s['instruction'].strip().lower()
        if key not in seen:
            seen.add(key)
            final_data.append(s)
            
    print(f"Augmented size: {len(final_data)}")
    
    save_data(final_data, out_path)
    print(f"Saved to {out_path}")
    print("\nIf you want to use this massive dataset, just overwrite CONVERSATIONAL_FLUENCY.jsonl with it!")

if __name__ == "__main__":
    main()
