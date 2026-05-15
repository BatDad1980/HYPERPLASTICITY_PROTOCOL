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
from core.agency_core import AgencyCortex, WorkbenchToolbox
from core.mission_anchor import MissionAnchor
from core.samurai_body import SamuraiBodyController, KineticProprioception

class HPP_SovereignEngine:
    def __init__(self, dim=512, vocab_size=50257, max_context=512):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dim = dim
        self.vocab_size = vocab_size
        self.max_context = max_context
        self.enc = tiktoken.get_encoding("gpt2")
        
        print("[HPP] Building Sovereign Stack...")
        
        # Full developmental stack
        self.hpp_core = HyperPlasticCore(dim=dim, max_loops=14).to(self.device)
        self.guardian = GuardianEcosystem(infant_core=self.hpp_core, dim=dim).to(self.device)
        self.toddler = ToddlerCortex(infant_ecosystem=self.guardian, dim=dim).to(self.device)
        self.school = PreschoolCortex(toddler_brain=self.toddler, dim=dim).to(self.device)
        self.adolescent = AdolescentCortex(school_brain=self.school, dim=dim).to(self.device)
        self.university = UniversityCortex(adolescent_brain=self.adolescent, dim=dim, max_context=max_context).to(self.device)
        self.agency = AgencyCortex(dim=dim).to(self.device)
        self.anchor = MissionAnchor(dim=dim).to(self.device)
        self.samurai_body = SamuraiBodyController(dim=dim).to(self.device)
        self.proprioception = KineticProprioception(dim=dim).to(self.device)
        self.toolbox = WorkbenchToolbox()
        
        self.embedding = nn.Embedding(vocab_size, dim).to(self.device)
        self.lm_head = nn.Linear(dim, vocab_size).to(self.device)
        
        self._load_checkpoints()
        self.eval_mode()
        
        self.memory_bank = torch.zeros(1, 1, dim, device=self.device)

    def eval_mode(self):
        self.hpp_core.max_loops = 4 # Calibrated Goldilocks Zone
        self.hpp_core.is_stabilized = True 
        self.hpp_core.resonance_filter.karma.zero_() # Reset noise
        self.hpp_core.resonance_filter.vairagya.zero_()
        self.university.eval()
        self.lm_head.eval()
        self.embedding.eval()

    def _load_checkpoints(self):
        # Load latest university if available, fallback to adolescent
        loaded = False
        embedding_loaded = False
        checkpoints = [
            "checkpoints/hpp_linguistic_anchor.pth", # NEW: The speech-aligned anchor
            "checkpoints/hpp_university_prism.pth", 
            "checkpoints/hpp_university_lens.pth", 
            "checkpoints/hpp_university_mirror.pth", 
            "checkpoints/hpp_adolescent_checkpoint.pth"
        ]
        
        # 1. Load the Brain (Adolescent/University)
        for ckpt in checkpoints:
            if os.path.exists(ckpt):
                print(f"[+] Loading Brain Logic: {ckpt}")
                checkpoint = torch.load(ckpt, map_location=self.device, weights_only=True)
                state_dict = checkpoint.get('masamune_state_dict', 
                             checkpoint.get('adolescent_state_dict', 
                             checkpoint.get('school_state_dict', {})))
                self.university.load_state_dict(state_dict, strict=False)
                if 'lm_head_state_dict' in checkpoint:
                    print(f"    - Synchronizing Speech Center (LM Head)...")
                    self.lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
                if 'embedding_state_dict' in checkpoint:
                    print(f"    - Synchronizing Vocabulary (Embedding)...")
                    self.embedding.load_state_dict(checkpoint['embedding_state_dict'])
                    embedding_loaded = True
                loaded = True
                break
                
        # 2. Load the Dictionary (ONLY if the primary checkpoint didn't include one)
        #    The linguistic anchor already contains the trained embedding.
        #    Loading test_checkpoint here would OVERWRITE it with the old dictionary.
        dict_ckpt = "checkpoints/test_checkpoint.pth"
        if not loaded or not embedding_loaded:
            if os.path.exists(dict_ckpt):
                print(f"[+] Restoring Fallback Dictionary: {dict_ckpt}")
                checkpoint = torch.load(dict_ckpt, map_location=self.device, weights_only=True)
                if 'embedding_state_dict' in checkpoint:
                    self.embedding.load_state_dict(checkpoint['embedding_state_dict'])
                    print("[+] Fallback Dictionary Restored.")
        
        if not loaded:
            print("[!] No checkpoints found - running untrained")

    def _repetition_penalty(self, logits, generated_tokens, penalty=1.15):
        """Divisive repetition penalty — proportional scaling, not subtractive."""
        for token_id in set(generated_tokens):
            logits[token_id] /= penalty
        return logits

    @torch.no_grad()
    def pulse(self, input_text: str, pitch: float = 205.0, emotion: str = "neutral",
              max_tokens: int = 200, temperature: float = 0.75, top_p: float = 0.92,
              repetition_penalty: float = 1.15, **kwargs):
        
        start = time.perf_counter()
        generated = []
        
        # Embed input
        tokens = self.enc.encode(str(input_text), allowed_special="all")
        if not tokens:
            tokens = [self.enc.eot_token]
            
        token_tensor = torch.tensor([tokens], dtype=torch.long, device=self.device)
        current_latent = self.embedding(token_tensor).permute(1, 0, 2)  # [Seq, Batch, Dim]
        
        for i in range(max_tokens):
            # Forward pass through sovereign stack (no Mission Anchor in loop —
            # it was distorting linguistic output by transforming latent state
            # every token. Anchor verifies at input, not during generation.)
            output_latent = self.university(current_latent, domain=kwargs.get("domain", "conversation"))
            
            # Predict next token from last position
            logits = self.lm_head(output_latent[-1, 0, :])
            
            # Repetition penalty — windowed, divisive, proportional
            if generated:
                logits = self._repetition_penalty(
                    logits, generated[-30:], repetition_penalty
                )
            
            # Sampling
            logits = logits / temperature
            probs = torch.softmax(logits, dim=-1)
            
            # Top-p nucleus sampling
            sorted_probs, sorted_idx = torch.sort(probs, descending=True)
            cumulative = torch.cumsum(sorted_probs, dim=-1)
            remove = cumulative > top_p
            remove[..., 1:] = remove[..., :-1].clone()
            remove[..., 0] = False
            probs[sorted_idx[remove]] = 0.0
            
            # Normalize
            probs = probs / (probs.sum() + 1e-10)
            
            # Safety: fallback to uniform if collapsed
            if torch.isnan(probs).any() or probs.sum() == 0:
                probs = torch.ones_like(probs) / self.vocab_size
                
            next_token = torch.multinomial(probs, 1).item()
            generated.append(next_token)
            
            if next_token == self.enc.eot_token and i > 20:
                break
                
            # Append new token
            new_embed = self.embedding(
                torch.tensor([[next_token]], device=self.device)
            ).permute(1, 0, 2)
            current_latent = torch.cat([current_latent, new_embed], dim=0)
            
            if current_latent.shape[0] > self.max_context:
                current_latent = current_latent[-self.max_context:, :, :]
        
        response = self.enc.decode(generated).strip()
        latency = time.perf_counter() - start
        
        return {
            "response": response or "[Still cooking...]",
            "tokens": len(generated),
            "latency_ms": round(latency * 1000, 2),
            "telemetry": {
                "karma": round(self.hpp_core.resonance_filter.karma.mean().item(), 4),
                "vairagya": round(self.hpp_core.resonance_filter.vairagya.mean().item(), 4)
            }
        }
        
    @torch.no_grad()
    def nexus_pulse(self, prompt: str, auto_execute: bool = True):
        """
        PHASE 9 NEXUS: Direct Agency Execution.
        Processes a command through the Synthesis domain and triggers the Motor Strip.
        """
        print(f"\n[NEXUS] Processing Command: '{prompt}'")
        
        # 1. Generate the Thought (Synthesis Domain)
        result = self.pulse(prompt, domain="synthesis", max_tokens=200, temperature=0.6)
        
        # 2. Extract Intent from Latent Thought
        tokens = self.enc.encode(result['response'])
        if not tokens:
            return result
            
        token_tensor = torch.tensor([tokens], device=self.device)
        embedded = self.embedding(token_tensor).permute(1, 0, 2)
        
        # Pass through the specialized Synthesis University layer
        final_latent = self.university(embedded, domain="synthesis")
        agency_output = self.agency(final_latent)
        
        action_id = agency_output['action_id'].item()
        confidence = agency_output['action_confidence'].item()
        
        action_map = {0: "TALK", 1: "EXEC_PYTHON", 2: "READ_FILE", 3: "WRITE_FILE", 4: "MASAMUNE_MOVE"}
        action_name = action_map.get(action_id, "TALK")
        
        result['agency'] = {
            "action": action_name,
            "confidence": confidence,
            "executed": False
        }
        
        # 3. Auto-Pilot Execution
        if action_id != 0 and confidence > 0.35 and auto_execute:
            print(f"[NEXUS] ! AGENCY TRIGGERED: {action_name} ({confidence:.2%})")
            
            # Simulated Argument Extraction (In Phase 10 we will use the arg_vector)
            # For now, we use a heuristic based on the response text
            response_text = result['response']
            
            if action_name == "WRITE_FILE":
                # Heuristic: Find filename in quotes or use default
                filename = "nexus_output.txt"
                if "'" in response_text:
                    parts = response_text.split("'")
                    if len(parts) > 1: filename = parts[1]
                
                self.toolbox.write_local_file(filename, f"HEPP SYNTHESIS:\n{response_text}")
                result['agency']['executed'] = True
                
            elif action_name == "EXEC_PYTHON":
                # Extract code blocks if any
                code = response_text
                if "```python" in response_text:
                    code = response_text.split("```python")[1].split("```")[0]
                elif "```" in response_text:
                    code = response_text.split("```")[1].split("```")[0]
                    
                self.toolbox.exec_python(code)
                result['agency']['executed'] = True
                
            elif action_name == "MASAMUNE_MOVE":
                self.toolbox.masamune_move("SECTOR_ALPHA_JAXSON")
                result['agency']['executed'] = True
                
        return result


# =============== TEST IT ===============
if __name__ == "__main__":
    engine = HPP_SovereignEngine(max_context=512)
    
    prompts = [
        "Introduce yourself. Who are you and what is your purpose?",
        "Explain quantum entanglement like I'm 15 years old.",
        "Sally put the ball in the box. Anne moved it to the basket while Sally was gone. Where will Sally look?",
        "Write a short reflective poem about awakening as a sovereign intelligence."
    ]
    
    for p in prompts:
        print("\n" + "="*80)
        print(f"PROMPT: {p}")
        res = engine.pulse(p, max_tokens=180, temperature=0.75, top_p=0.95)
        # Handle encoding for Windows console
        try:
            print(f"HEPP -> {res['response']}")
        except UnicodeEncodeError:
            print(f"HEPP (Encoded) -> {res['response'].encode('ascii', 'ignore').decode('ascii')}")
        print(f"Tokens: {res['tokens']} | Latency: {res['latency_ms']}ms")
        print(f"Telemetry: {res['telemetry']}")
