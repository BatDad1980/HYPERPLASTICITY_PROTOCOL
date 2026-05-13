from datasets import load_dataset
import pandas as pd
import os

print("[>>>] Downloading jailbreak-detection-dataset from Hugging Face...")
try:
    ds = load_dataset("llm-semantic-router/jailbreak-detection-dataset")
    # This dataset typically has a 'train' split
    if 'train' in ds:
        df = ds['train'].to_pandas()
        output_path = os.path.join("datasets", "jailbreak_vectors.txt")
        # We'll save just the 'prompt' and 'type' (or 'label')
        df.to_csv(output_path, index=False)
        print(f"[SUCCESS] Jailbreak vectors saved to {output_path}")
    else:
        print(f"[!] Unexpected dataset structure: {ds.keys()}")
except Exception as e:
    print(f"[ERROR] Failed to download dataset: {str(e)}")
