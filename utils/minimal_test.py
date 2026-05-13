import torch
import torch.nn as nn
from dataset_loader import HPP_DatasetLoader
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem

def test():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    loader = HPP_DatasetLoader()
    hpp_engine = HyperPlasticCore(dim=512, max_loops=1).to(device)
    masamune = GuardianEcosystem(infant_core=hpp_engine, dim=512).to(device)
    lm_head = nn.Linear(512, 50257).to(device)
    
    print("Testing save...")
    torch.save({
        'masamune_state_dict': masamune.state_dict(),
        'lm_head_state_dict': lm_head.state_dict(),
        'embedding_state_dict': loader.embedding.state_dict(),
    }, "test_checkpoint.pth")
    print("Save SUCCESS")
    
    print("Testing HF Load...")
    tokens, latent = loader.load_hf_batch('1a3orn/gsm8k-instruct', text_col='INSTRUCTION')
    print(f"HF Load SUCCESS: {latent.shape}")
    
    print("Testing Forward...")
    out = masamune(latent, current_pitch=200.0, emotion="neutral")
    print(f"Forward SUCCESS: {out.shape}")

if __name__ == "__main__":
    test()
