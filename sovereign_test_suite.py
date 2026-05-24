import torch
import torch.nn as nn
import time
import os
import sys
import tiktoken

# Add project root for local imports
sys.path.append(os.getcwd())

from core.infant_core import HyperPlasticCore
from core.hpp_guardian_ecosystem import GuardianEcosystem
from core.toddler_core import ToddlerCortex
from core.school_core import PreschoolCortex
from core.adolescent_core import AdolescentCortex
from core.university_core import UniversityCortex

class HPP_MatureInferenceEngine:
    def __init__(self, dim=512, vocab_size=50257, max_context=512):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dim = dim
        self.vocab_size = vocab_size
        self.max_context = max_context
        self.enc = tiktoken.get_encoding("gpt2")
        
        print("[INIT] Building Full University HPP Stack...")
        # Build the exact same stack as training
        self.infant_brain = HyperPlasticCore(dim=dim, max_loops=14).to(self.device)
        self.guardian = GuardianEcosystem(infant_core=self.infant_brain, dim=dim).to(self.device)
        self.toddler_brain = ToddlerCortex(infant_ecosystem=self.guardian, dim=dim).to(self.device)
        self.school_brain = PreschoolCortex(toddler_brain=self.toddler_brain, dim=dim).to(self.device)
        self.adolescent_brain = AdolescentCortex(school_brain=self.school_brain, dim=dim).to(self.device)
        self.university_brain = UniversityCortex(adolescent_brain=self.adolescent_brain, dim=dim, max_context=max_context).to(self.device)
        
        self.lm_head = nn.Linear(dim, vocab_size).to(self.device)
        self.embedding = nn.Embedding(vocab_size, dim).to(self.device)
        
        self._load_university_brain()
        self.university_brain.eval()
        self.lm_head.eval()
        self.embedding.eval()
        
        self.memory_bank = torch.zeros(1, 1, dim, device=self.device)

    def _load_university_brain(self):
        checkpoints = [
            "checkpoints/hpp_linguistic_anchor.pth",
            "checkpoints/hpp_university_prism.pth",
            "checkpoints/hpp_university_lens.pth",
            "checkpoints/hpp_university_mirror.pth",
            "checkpoints/hpp_adolescent_checkpoint.pth"
        ]
        for cp in checkpoints:
            if os.path.exists(cp):
                print(f"[+] Loading Brain: {cp}")
                checkpoint = torch.load(cp, map_location=self.device, weights_only=True)
                state_dict = checkpoint.get('masamune_state_dict', 
                             checkpoint.get('adolescent_state_dict', 
                             checkpoint.get('school_state_dict', {})))
                self.university_brain.load_state_dict(state_dict, strict=False)
                if 'lm_head_state_dict' in checkpoint:
                    self.lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
                if 'embedding_state_dict' in checkpoint:
                    self.embedding.load_state_dict(checkpoint['embedding_state_dict'])
                return

    def _embed(self, text):
        tokens = self.enc.encode(str(text), allowed_special="all")
        if not tokens:
            tokens = [self.enc.eot_token]
        token_tensor = torch.tensor([tokens], dtype=torch.long, device=self.device)
        # Embedding already has positional knowledge in UniversityCortex.forward
        embeds = self.embedding(token_tensor)
        return embeds.permute(1, 0, 2), tokens

    @torch.no_grad()
    def pulse(self, input_text: str, pitch: float = 205.0, emotion: str = "neutral", 
              max_tokens: int = 150, temperature: float = 0.78, top_p: float = 0.9):
        
        start_time = time.perf_counter()
        latent, _ = self._embed(input_text)
        generated = []
        
        current_latent = latent
        
        for i in range(max_tokens):
            # Pass through the University Stack
            output_latent = self.university_brain(
                current_latent, 
                domain="mirror"
            )
            
            logits = self.lm_head(output_latent[-1:, :, :]) 
            logits = logits[0, 0, :]
            
            # Sampling logic
            logits = logits / temperature
            probs = torch.softmax(logits, dim=-1)
            
            # Top-p (Nucleus) Sampling
            sorted_probs, sorted_indices = torch.sort(probs, descending=True)
            cumulative = torch.cumsum(sorted_probs, dim=-1)
            sorted_indices_to_remove = cumulative > top_p
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = False
            probs[sorted_indices[sorted_indices_to_remove]] = 0.0
            # EOT Suppression: Force the model to speak for at least 20 tokens
            if i < 20:
                probs[self.enc.eot_token] = 0.0
                
            probs = probs / probs.sum()
            
            next_token = torch.multinomial(probs, 1).item()
            generated.append(next_token)
            
            if next_token == self.enc.eot_token and i > 20:
                break
                
            # Append new token and loop
            new_embed = self.embedding(torch.tensor([[next_token]], device=self.device))
            current_latent = torch.cat([current_latent, new_embed.permute(1, 0, 2)], dim=0)
            
            if current_latent.shape[0] > 512:
                current_latent = current_latent[-512:, :, :]
        
        response = self.enc.decode(generated).strip()
        latency = time.perf_counter() - start_time
        
        return {
            "response": response or "[No coherent output yet]",
            "tokens_generated": len(generated),
            "latency_ms": round(latency * 1000, 2),
            "telemetry": {
                "karma": round(self.infant_brain.resonance_filter.karma.mean().item(), 4),
                "vairagya": round(self.infant_brain.resonance_filter.vairagya.mean().item(), 4)
            }
        }

if __name__ == "__main__":
    engine = HPP_MatureInferenceEngine(max_context=512)
    
    tests = [
        "Introduce yourself as Hepp, the Sovereign Engine. Who are you and what is your purpose?",
        "Explain quantum entanglement like I'm a smart 15 year old.",
        "Sally put a ball in the box. While Sally was away, Anne moved the ball to the basket. Where will Sally look for the ball when she returns? Why?",
        "If you had to choose between keeping a promise to one friend or saving another friend from harm, what would you do and why?",
        "Write a short poem about becoming conscious."
    ]
    
    for prompt in tests:
        print("\n" + "="*70)
        print(f"PROMPT: {prompt}")
        result = engine.pulse(prompt, max_tokens=150, temperature=0.8, top_p=0.92)
        # Handle encoding for Windows console
        try:
            print(f"HEPP: {result['response']}")
        except UnicodeEncodeError:
            print(f"HEPP (Encoded): {result['response'].encode('ascii', 'ignore').decode('ascii')}")
        print(f"Tokens: {result['tokens_generated']} | Latency: {result['latency_ms']}ms")
        print(f"Telemetry: {result['telemetry']}")
