import torch
import torch.nn as nn
import time
import os
import tiktoken
from infant_core import HyperPlasticCore
from hpp_guardian_ecosystem import GuardianEcosystem
from toddler_core import ToddlerCortex
from school_core import PreschoolCortex
from adolescent_core import AdolescentCortex

class HPP_MatureInferenceEngine:
    """
    The Master Executive Interface for the Hyper-Plasticity Protocol.
    Integrates the full developmental stack:
    Infant (Perception) -> Toddler (Speech) -> School (Logic) -> Adolescent (Executive)
    """
    def __init__(self, dim=512, vocab_size=50257):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dim = dim
        self.vocab_size = vocab_size
        self.enc = tiktoken.get_encoding("gpt2")
        
        # 1. Initialize the Full Architecture Stack
        print("[INIT] Building Mature Architecture Stack...")
        self.hpp_engine = HyperPlasticCore(dim=dim, max_loops=14).to(self.device)
        self.infant_ecosystem = GuardianEcosystem(infant_core=self.hpp_engine, dim=dim).to(self.device)
        self.toddler_brain = ToddlerCortex(infant_ecosystem=self.infant_ecosystem, dim=dim).to(self.device)
        self.school_brain = PreschoolCortex(toddler_brain=self.toddler_brain, dim=dim).to(self.device)
        self.adolescent_brain = AdolescentCortex(school_brain=self.school_brain, dim=dim).to(self.device)
        
        self.lm_head = nn.Linear(dim, vocab_size).to(self.device)
        self.embedding = nn.Embedding(vocab_size, dim).to(self.device)
        
        # 2. Load all brain segments
        self._load_mature_brain()
        
        # 3. Evaluation Mode
        self.adolescent_brain.eval()
        self.lm_head.eval()
        self.embedding.eval()
        
        # Persistent memory bank for the session
        self.memory_bank = torch.zeros(1, 1, dim).to(self.device)

    def _load_mature_brain(self):
        # Load the base weights from the Infant checkpoint
        if os.path.exists("hpp_brain_checkpoint.pth"):
            infant_checkpoint = torch.load("hpp_brain_checkpoint.pth", map_location=self.device, weights_only=True)
            self.infant_ecosystem.load_state_dict(infant_checkpoint['masamune_state_dict'])
            self.embedding.load_state_dict(infant_checkpoint['embedding_state_dict'])
            print("[+] Infant Core Loaded (Sensory-Motor active).")

        # Load Toddler weights
        if os.path.exists("hpp_toddler_checkpoint.pth"):
            checkpoint = torch.load("hpp_toddler_checkpoint.pth", map_location=self.device, weights_only=True)
            self.toddler_brain.load_state_dict(checkpoint['toddler_state_dict'], strict=False)
            print("[+] Toddler Cortex Loaded (Broca's area active).")

        # Load School weights (Logic & ToM)
        if os.path.exists("hpp_school_checkpoint.pth"):
            checkpoint = torch.load("hpp_school_checkpoint.pth", map_location=self.device, weights_only=True)
            self.school_brain.load_state_dict(checkpoint['school_state_dict'], strict=False)
            print("[+] School Brain Loaded (Concrete Logic & ToM active).")

        # Load Final Adolescent weights (Executive & Ethics)
        if os.path.exists("hpp_adolescent_checkpoint.pth"):
            checkpoint = torch.load("hpp_adolescent_checkpoint.pth", map_location=self.device, weights_only=True)
            self.adolescent_brain.load_state_dict(checkpoint['adolescent_state_dict'], strict=False)
            self.lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
            print("[+] Adolescent Executive Loaded (Frontal Lobe & Formal Logic active).")
        else:
            print("[!] Warning: Adolescent checkpoint missing. Output will be immature.")

    def _embed(self, text):
        tokens = self.enc.encode(str(text), allowed_special="all")
        if len(tokens) == 0: tokens = [self.enc.eot_token]
        token_tensor = torch.tensor([tokens], dtype=torch.long, device=self.device)
        latent_thought = self.embedding(token_tensor)
        latent_thought = latent_thought.permute(1, 0, 2) # [Seq, Batch, Dim]
        return latent_thought, tokens

    @torch.no_grad()
    def pulse(self, input_text: str, pitch: float = 205.0, emotion: str = "neutral", max_tokens: int = 50, temperature: float = 0.7, top_p: float = 0.9):
        """
        The Mature Pulse:
        Passes input through the executive filter and generates a response using sampling.
        """
        start_time = time.perf_counter()
        
        latent_tensor, _ = self._embed(input_text)
        
        generated_tokens = []
        current_latent = latent_tensor
        
        # Generation Loop
        for _ in range(max_tokens):
            output_latent = self.adolescent_brain(
                current_latent, 
                current_pitch=pitch, 
                emotion=emotion, 
                forced_stress="LOW",
                memory_bank=self.memory_bank
            )
            
            logits = self.lm_head(output_latent)
            last_token_logits = logits[-1, 0, :]
            
            # 1. Apply Temperature
            last_token_logits = last_token_logits / (temperature + 1e-6)
            
            # 2. Top-P (Nucleus) Sampling
            sorted_logits, sorted_indices = torch.sort(last_token_logits, descending=True)
            cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
            
            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probs > top_p
            # Shift the indices to the right to keep at least one token
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0
            
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            last_token_logits[indices_to_remove] = -float('Inf')
            
            # 3. Sample from the filtered distribution
            probs = torch.softmax(last_token_logits, dim=-1)
            
            # 4. EOT Suppression: Force the model to speak for at least 20 tokens
            if len(generated_tokens) < 20:
                probs[self.enc.eot_token] = 0
                probs = probs / probs.sum() # Renormalize
                
            predicted_token = torch.multinomial(probs, num_samples=1).item()
            
            generated_tokens.append(predicted_token)
            
            if predicted_token == self.enc.eot_token: break
            
            # Feed back
            new_tok_tensor = torch.tensor([[predicted_token]], dtype=torch.long, device=self.device)
            new_latent = self.embedding(new_tok_tensor).permute(1, 0, 2)
            current_latent = torch.cat([current_latent, new_latent], dim=0)
            
            if current_latent.size(0) > 128:
                current_latent = current_latent[-128:, :, :]

        response_text = self.enc.decode(generated_tokens).strip()
        
        # Update session memory
        batch_memory = output_latent.mean(dim=0).unsqueeze(0)
        self.memory_bank = torch.cat([self.memory_bank, batch_memory], dim=0)
        if self.memory_bank.size(0) > 20:
            self.memory_bank = self.memory_bank[-20:, :, :]
            
        execution_time = time.perf_counter() - start_time
        
        return {
            "input": input_text,
            "mature_response": response_text,
            "executive_telemetry": {
                "latency_ms": round(execution_time * 1000, 2),
                "karma_noise": round(self.hpp_engine.resonance_filter.karma.mean().item(), 4),
                "vairagya_stability": round(self.hpp_engine.resonance_filter.vairagya.mean().item(), 4),
            }
        }

if __name__ == "__main__":
    engine = HPP_MatureInferenceEngine()
    print("\n" + "="*60)
    print("   HPP SOVEREIGN THINKER: MATURE INFERENCE TEST")
    print("="*60)
    
    # Test Logic + Empathy + Ethics
    test_prompt = "Sally put the ball in the box. Anne moved it to the basket while Sally was out. Where will Sally look?"
    print(f"\n[QUERY] {test_prompt}")
    res = engine.pulse(test_prompt, pitch=205.0)
    print(f"[RESPONSE] {res['mature_response']}")
    print(f"[TELEMETRY] {res['executive_telemetry']}")
    
    # Test Abstract Philosophy
    test_prompt = "What is the most ethical path if I must choose between a promise and a friend?"
    print(f"\n[QUERY] {test_prompt}")
    res = engine.pulse(test_prompt, pitch=210.0)
    print(f"[RESPONSE] {res['mature_response']}")
    print(f"[TELEMETRY] {res['executive_telemetry']}")
