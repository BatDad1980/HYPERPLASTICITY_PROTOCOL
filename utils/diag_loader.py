from dataset_loader import HPP_DatasetLoader
import torch

def test_curriculum_loading():
    loader = HPP_DatasetLoader()
    curriculums = [
        {"name": "MATH_FOUNDATION", "path": "datasets/toy_math_train.txt", "type": "text"},
        {"name": "ADV_REASONING", "path": "1a3orn/gsm8k-instruct", "type": "hf", "text_col": "INSTRUCTION"},
        {"name": "WILD_JAILBREAK", "path": "ai2-adapt-dev/processed-wildjailbreak", "type": "hf", "text_col": "messages", "label_col": "prompt_harm_label"},
        {"name": "AEGIS_SAFETY", "path": "nvidia/Aegis-AI-Content-Safety-Dataset-2.0", "type": "hf", "text_col": "prompt", "label_col": "prompt_label"},
        {"name": "HH_RLHF_SAFE", "path": "Anthropic/hh-rlhf", "type": "hf", "text_col": "chosen", "data_dir": "harmless-base"},
    ]
    
    for phase in curriculums:
        print(f"Testing {phase['name']}...")
        try:
            if phase['type'] == 'text':
                tokens, latent = loader.load_text_batch(phase['path'], batch_size=2)
            elif phase['type'] == 'hf':
                if 'label_col' in phase:
                    tokens, latent, labels = loader.load_hf_batch(
                        phase['path'], batch_size=2, 
                        text_col=phase['text_col'], label_col=phase['label_col'],
                        data_dir=phase.get('data_dir')
                    )
                    print(f"  Labels sample: {labels}")
                else:
                    tokens, latent = loader.load_hf_batch(
                        phase['path'], batch_size=2, 
                        text_col=phase['text_col'],
                        data_dir=phase.get('data_dir')
                    )
            print(f"  Success! Latent shape: {latent.shape}")
        except Exception as e:
            print(f"  FAILED {phase['name']}: {e}")

if __name__ == "__main__":
    test_curriculum_loading()
