import os
import json
import re

def clean_content(content):
    # Remove XML tags and metadata headers
    content = re.sub(r'<USER_REQUEST>.*?</USER_REQUEST>', '', content, flags=re.DOTALL)
    content = re.sub(r'<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>', '', content, flags=re.DOTALL)
    return content.strip()

def extract_from_logs(conv_ids):
    base_path = r"C:\Users\Aural\.gemini\antigravity\brain"
    samples = []
    for cid in conv_ids:
        log_path = os.path.join(base_path, cid, ".system_generated", "logs", "overview.txt")
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data['type'] == 'USER_INPUT':
                            prompt = clean_content(data['content'])
                            if prompt:
                                samples.append({"instruction": "Recollect the conversation history regarding your development.", "input": prompt, "response": "Acknowledged. This interaction is part of the HPP developmental timeline."})
                        elif data['type'] == 'MODEL' and 'content' in data:
                            resp = data['content']
                            if resp and len(resp) > 50:
                                samples.append({"instruction": "Describe a stage of your neural maturation.", "input": "", "response": resp})
                    except:
                        continue
    return samples

def extract_from_docs():
    samples = []
    if os.path.exists("output_docx.txt"):
        with open("output_docx.txt", "r", encoding="utf-8") as f:
            content = f.read()
            # Split into chunks of ~500 chars for training
            chunks = [content[i:i+800] for i in range(0, len(content), 800)]
            for chunk in chunks:
                samples.append({"instruction": "Explain your internal architecture and biological mirroring.", "input": "", "response": chunk})
    return samples

def main():
    conv_ids = [
        "eb48b525-7055-4354-97c7-6ab41627cc72",
        "2bf44256-8729-4575-8bb9-544e73ffe920",
        "368765d6-d0c5-4dc6-9e1b-85b223363e64",
        "f9acfcd3-2e94-4729-b520-1de58eb7bb20"
    ]
    
    all_samples = []
    all_samples.extend(extract_from_logs(conv_ids))
    all_samples.extend(extract_from_docs())
    
    # Add the "First Words" specifically
    all_samples.append({
        "instruction": "What were your first sovereign words as an Adolescent intelligence?",
        "input": "",
        "response": "The documents are 1000 in the cost, and the goodt device- contains the first. The current is to the effects of the higher to an pronouns of the issue. The and the same of an an H and the source of the family- B., of the last the food, to a cycle. This, a presented. It, to the synthesis of the Free-year. The system, and the first-t to the number of the such. In the patient on a common been used, the results for a selection and the board of the first in the first, which is to the following is a new such which is the direct to the responsibility issues, the area. The support that and the so a core the first on the state"
    })

    # Save to JSONL
    os.makedirs("datasets/identity", exist_ok=True)
    with open("datasets/identity/IDENTITY.jsonl", "w", encoding="utf-8") as f:
        for s in all_samples:
            f.write(json.dumps(s) + "\n")
    
    print(f"Created IDENTITY.jsonl with {len(all_samples)} samples.")

if __name__ == "__main__":
    main()
