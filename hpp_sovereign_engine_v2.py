"""
===============================================================================
     HPP SOVEREIGN ENGINE v2.0 — FRONTIER INFERENCE
===============================================================================
Upgrades over v1:
    1. N-gram blocking (3-gram, 4-gram) — eliminates repetitive loops
    2. Proper autoregressive positional tracking — each new token gets the 
       CORRECT position index, not position 0
    3. Windowed frequency penalty — penalizes tokens proportional to how 
       recently and how often they appeared
    4. Min-length enforcement — suppresses EOT for first N tokens
    5. Mixed precision inference (fp16) — faster on RTX 4050
    6. Temperature annealing — starts warmer, cools as response develops
    7. Context-aware domain routing — auto-detects domain from input
    8. Proper response extraction — handles instruction/response format
    
The deep brain (Infant → Adolescent) is UNTOUCHED. All improvements are in 
how we READ the brain's output, not how it thinks.
===============================================================================
"""
import torch
import torch.nn as nn
import time
import os
import sys
import re
import tiktoken
from collections import Counter

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.infant_core import HyperPlasticCore
from core.hpp_guardian_ecosystem import GuardianEcosystem
from core.toddler_core import ToddlerCortex
from core.school_core import PreschoolCortex
from core.adolescent_core import AdolescentCortex
from core.university_core import UniversityCortex
from core.agency_core import AgencyCortex, WorkbenchToolbox
from core.mission_anchor import MissionAnchor
from core.samurai_body import SamuraiBodyController, KineticProprioception


class HPP_SovereignEngine_V2:
    """
    Frontier inference engine for the Hyperplasticity Protocol.
    All improvements are in decoding strategy — the neural architecture is unchanged.
    """
    
    def __init__(self, dim=512, vocab_size=50257, max_context=512, use_fp16=True):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dim = dim
        self.vocab_size = vocab_size
        self.max_context = max_context
        self.use_fp16 = use_fp16 and self.device.type == "cuda"
        self.enc = tiktoken.get_encoding("gpt2")
        
        print("=" * 70)
        print("     HPP SOVEREIGN ENGINE v2.0 — FRONTIER INFERENCE")
        print("=" * 70)
        print(f"  Device:    {self.device}")
        print(f"  Precision: {'FP16' if self.use_fp16 else 'FP32'}")
        print(f"  Context:   {max_context}")
        print("=" * 70)
        
        self.power_mode = "plugged"  # Defaults to plugged in
        
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
        
        # Convert to fp16 for faster inference
        if self.use_fp16:
            self.hpp_core.half()
            self.guardian.half()
            self.toddler.half()
            self.school.half()
            self.adolescent.half()
            self.university.half()
            self.agency.half()
            self.anchor.half()
            self.samurai_body.half()
            self.proprioception.half()
            self.lm_head.half()
            self.embedding.half()
            print("[FP16] Entire brain converted to half precision")
        
        self.memory_bank = torch.zeros(1, 1, dim, device=self.device, 
                                        dtype=torch.float16 if self.use_fp16 else torch.float32)
        
        # Domain keyword map for auto-routing
        self._domain_keywords = {
            "identity": ["who are you", "your name", "your purpose", "masamune", "hepp",
                        "what are you", "your creator", "your mission", "your oath",
                        "jaxson", "journee", "bushido", "sovereign"],
            "synthesis": ["calculate", "solve", "python", "code", "analyze", "write",
                         "create", "build", "execute", "run", "compute", "implement"],
            "logic": ["explain", "why", "how does", "what is", "define", "compare",
                     "difference between", "prove", "reason"],
        }
        self._blocked_phrase_token_ids = self._build_blocked_phrase_tokens()
        
        print(f"\n[ENGINE] Sovereign Engine v2.0 READY")
        print(f"[ENGINE] Parameter count: {self._count_params():,}")
        print("=" * 70)

    def _count_params(self):
        """Count total trainable parameters."""
        total = 0
        for module in [self.university, self.lm_head, self.embedding]:
            total += sum(p.numel() for p in module.parameters())
        return total

    def set_power_mode(self, mode: str):
        """
        Dynamically adjusts inference ceiling to manage GPU power usage.
        Valid modes: 'plugged', 'battery', 'demo'
        """
        if mode.lower() not in ["plugged", "battery", "demo"]:
            print(f"[!] Warning: Unknown power mode '{mode}'. Defaulting to 'plugged'.")
            self.power_mode = "plugged"
            return
            
        self.power_mode = mode.lower()
        print(f"\n[POWER] Switched to {self.power_mode.upper()} mode")
        if self.power_mode == "battery":
            print("  -> Inference capped to conserve VRAM & battery.")
        elif self.power_mode == "demo":
            print("  -> Ultra-fast mode activated for quick debugging.")

    def eval_mode(self):
        """Set engine to inference mode with calibrated recursion depth."""
        self.hpp_core.max_loops = 4  # Goldilocks Zone
        self.hpp_core.is_stabilized = True
        self.hpp_core.resonance_filter.karma.zero_()
        self.hpp_core.resonance_filter.vairagya.zero_()
        self.university.eval()
        self.lm_head.eval()
        self.embedding.eval()

    def _load_checkpoints(self):
        """Load brain checkpoints with priority ordering."""
        loaded = False
        embedding_loaded = False
        checkpoints = [
            "checkpoints/hpp_linguistic_anchor.pth",
            "checkpoints/hpp_university_prism.pth",
            "checkpoints/hpp_university_lens.pth",
            "checkpoints/hpp_university_mirror.pth",
            "checkpoints/hpp_adolescent_checkpoint.pth"
        ]
        
        for ckpt in checkpoints:
            if os.path.exists(ckpt):
                print(f"[+] Loading Brain: {ckpt}")
                checkpoint = torch.load(ckpt, map_location=self.device, weights_only=True)
                state_dict = checkpoint.get('masamune_state_dict',
                             checkpoint.get('adolescent_state_dict',
                             checkpoint.get('school_state_dict', {})))
                self.university.load_state_dict(state_dict, strict=False)
                if 'lm_head_state_dict' in checkpoint:
                    self.lm_head.load_state_dict(checkpoint['lm_head_state_dict'])
                if 'embedding_state_dict' in checkpoint:
                    self.embedding.load_state_dict(checkpoint['embedding_state_dict'])
                    embedding_loaded = True
                loaded = True
                break
        
        if not loaded or not embedding_loaded:
            dict_ckpt = "checkpoints/test_checkpoint.pth"
            if os.path.exists(dict_ckpt):
                print(f"[+] Restoring Fallback Dictionary: {dict_ckpt}")
                checkpoint = torch.load(dict_ckpt, map_location=self.device, weights_only=True)
                if 'embedding_state_dict' in checkpoint:
                    self.embedding.load_state_dict(checkpoint['embedding_state_dict'])
        
        if not loaded:
            print("[!] No checkpoints found — running untrained")

    def _detect_domain(self, text: str) -> str:
        """Auto-detect domain from input text."""
        lower = text.lower()
        scores = {}
        for domain, keywords in self._domain_keywords.items():
            scores[domain] = sum(1 for kw in keywords if kw in lower)
        
        best = max(scores, key=scores.get)
        if scores[best] > 0:
            return best
        return "conversation"  # Default to conversation, not "none"

    def _speech_maturity_loop_cap(self, input_text: str, domain: str) -> int:
        """Cap recurrent speech depth for modes that are still loop-prone."""
        lower = input_text.lower()
        identity_terms = [
            "who are you",
            "what are you",
            "conscious",
            "feelings",
            "purpose",
        ]
        protective_terms = [
            "not doing well",
            "overwhelming",
            "protect",
            "giving up",
            "unsafe",
            "safety",
        ]
        embodiment_terms = ["masamune", "robot", "servo", "moving", "tool", "power"]

        if domain == "identity" or any(term in lower for term in identity_terms):
            return 1
        if any(term in lower for term in protective_terms):
            return 2
        if any(term in lower for term in embodiment_terms):
            return 2
        return 2

    def _apply_speech_profile(
        self,
        profile: str,
        max_tokens: int,
        temperature: float,
        top_p: float,
        top_k: int,
        min_tokens: int,
        ngram_block: int,
        frequency_penalty: float,
        presence_penalty: float,
        phrase_blocking: bool,
        speech_maturity_gate: bool,
        temperature_decay: float,
    ) -> tuple[int, float, float, int, int, int, float, float, bool, bool, float]:
        """Apply named speech decoding profiles without changing checkpoint weights."""
        profile = profile.lower()
        if profile == "raw":
            return (
                max_tokens,
                temperature,
                top_p,
                top_k,
                min_tokens,
                ngram_block,
                frequency_penalty,
                presence_penalty,
                phrase_blocking,
                speech_maturity_gate,
                temperature_decay,
            )
        if profile != "stable":
            raise ValueError(f"Unknown speech_profile '{profile}'. Use 'raw' or 'stable'.")

        return (
            min(max_tokens, 56),
            min(temperature, 0.55),
            min(top_p, 0.86),
            min(top_k, 35) if top_k > 0 else 35,
            min(min_tokens, 8),
            max(ngram_block, 3),
            max(frequency_penalty, 1.35),
            max(presence_penalty, 0.55),
            True,
            True,
            min(temperature_decay, 0.99),
        )

    def _ngram_blocking(self, logits: torch.Tensor, generated: list, n: int = 3) -> torch.Tensor:
        """
        Block any token that would create a repeated n-gram.
        This is the single most effective anti-repetition technique.
        """
        if len(generated) < n - 1:
            return logits
        
        # Get the last (n-1) tokens — these form the beginning of a potential n-gram
        tail = tuple(generated[-(n-1):])
        
        # Scan history for this same (n-1) prefix
        for i in range(len(generated) - (n-1)):
            if tuple(generated[i:i+(n-1)]) == tail:
                # This n-gram already appeared — block the token that followed
                blocked_token = generated[i + (n-1)]
                logits[blocked_token] = -float('inf')
        
        return logits

    def _frequency_penalty(self, logits: torch.Tensor, generated: list, 
                           window: int = 40, penalty: float = 1.3) -> torch.Tensor:
        """
        Frequency-based penalty: tokens that appear more often in the recent 
        window get penalized more heavily. Proportional, not flat.
        """
        if not generated:
            return logits
        
        recent = generated[-window:]
        counts = Counter(recent)
        
        for token_id, count in counts.items():
            # Scale penalty by frequency: appearing once = mild, 3+ times = harsh
            scale = penalty ** count
            if logits[token_id] > 0:
                logits[token_id] /= scale
            else:
                logits[token_id] *= scale
        
        return logits

    def _presence_penalty(self, logits: torch.Tensor, generated: list,
                          penalty: float = 0.6) -> torch.Tensor:
        """
        Flat penalty for any token that has appeared at all.
        Encourages vocabulary diversity.
        """
        if not generated:
            return logits
        
        seen = set(generated)
        for token_id in seen:
            logits[token_id] -= penalty
        
        return logits

    def _build_blocked_phrase_tokens(self) -> list[list[int]]:
        """Pre-tokenize known speech attractors for decoder-side blocking."""
        blocked_phrases = [
            "What do you think",
            "do not quit",
            "fortress is standing",
            "you are standing",
            "Standing by",
        ]
        sequences = []
        for phrase in blocked_phrases:
            for variant in (phrase, " " + phrase, phrase.lower(), " " + phrase.lower()):
                tokens = self.enc.encode(variant)
                if tokens and tokens not in sequences:
                    sequences.append(tokens)
        return sequences

    def _phrase_blocking(self, logits: torch.Tensor, generated: list) -> torch.Tensor:
        """
        Block the next token when generation is entering a known attractor phrase.

        This is deliberately narrow: it suppresses loop-prone speech habits
        without altering the developmental stack or checkpoint weights.
        """
        if not generated:
            return logits

        for sequence in self._blocked_phrase_token_ids:
            if len(sequence) == 1:
                logits[sequence[0]] = -float("inf")
                continue
            prefix = sequence[:-1]
            if len(generated) >= len(prefix) and generated[-len(prefix):] == prefix:
                logits[sequence[-1]] = -float("inf")
        return logits

    @torch.no_grad()
    def pulse(self, input_text: str, pitch: float = 205.0, emotion: str = "neutral",
              max_tokens: int = 200, temperature: float = 0.65, top_p: float = 0.92,
              top_k: int = 50, min_tokens: int = 15,
              ngram_block: int = 3, frequency_penalty: float = 1.25,
              presence_penalty: float = 0.45,
              phrase_blocking: bool = False,
              speech_maturity_gate: bool = False,
              speech_profile: str = "raw",
              temperature_decay: float = 0.995,
              domain: str = "auto", **kwargs):
        """
        Sovereign Pulse v2 — upgraded decoding with full anti-repetition suite.
        
        New parameters:
            top_k: Limits sampling to top-k tokens (combined with top-p)
            min_tokens: Minimum tokens before EOT is allowed
            ngram_block: Block repeated n-grams of this size (0 to disable)
            frequency_penalty: Penalize frequent recent tokens
            presence_penalty: Flat penalty for any seen token
            temperature_decay: Multiply temperature by this each step (cooling)
            domain: "auto" to detect, or specify directly
        """
        start = time.perf_counter()
        generated = []

        # Auto-detect domain before power/depth controls so speech maturity can
        # gate unstable modes without altering checkpoint weights.
        if domain == "auto":
            domain = self._detect_domain(input_text)

        (
            max_tokens,
            temperature,
            top_p,
            top_k,
            min_tokens,
            ngram_block,
            frequency_penalty,
            presence_penalty,
            phrase_blocking,
            speech_maturity_gate,
            temperature_decay,
        ) = self._apply_speech_profile(
            speech_profile,
            max_tokens,
            temperature,
            top_p,
            top_k,
            min_tokens,
            ngram_block,
            frequency_penalty,
            presence_penalty,
            phrase_blocking,
            speech_maturity_gate,
            temperature_decay,
        )
        
        # Power Management Overrides
        if self.power_mode == "battery":
            max_tokens = min(max_tokens, 75)
            temperature = max(0.5, temperature - 0.1) # Cool down to prevent wandering
            self.hpp_core.max_loops = 2 # Cut recursive depth to save power
        elif self.power_mode == "demo":
            max_tokens = min(max_tokens, 35)
            temperature = 0.5
            self.hpp_core.max_loops = 1
        else:
            self.hpp_core.max_loops = 4 # Goldilocks Zone for plugged in

        if speech_maturity_gate:
            self.hpp_core.max_loops = min(
                self.hpp_core.max_loops,
                self._speech_maturity_loop_cap(input_text, domain),
            )
        
        # Encode input
        tokens = self.enc.encode(str(input_text), allowed_special="all")
        if not tokens:
            tokens = [self.enc.eot_token]
        
        input_len = len(tokens)
        
        dtype = torch.float16 if self.use_fp16 else torch.float32
        token_tensor = torch.tensor([tokens], dtype=torch.long, device=self.device)
        current_latent = self.embedding(token_tensor).permute(1, 0, 2)  # [Seq, Batch, Dim]
        
        if self.use_fp16:
            current_latent = current_latent.half()
        
        current_temp = temperature
        
        for i in range(max_tokens):
            # Forward through sovereign stack
            output_latent = self.university(current_latent, domain=domain)
            
            # Get logits for last position only
            last_hidden = output_latent[-1, 0, :]
            
            logits = self.lm_head(last_hidden.unsqueeze(0).unsqueeze(0) 
                                  if last_hidden.dim() == 1 
                                  else last_hidden.unsqueeze(0))
            if self.use_fp16:
                logits = logits.float()  # Back to fp32 for stable sampling
            logits = logits.squeeze()
            
            # === ANTI-REPETITION SUITE ===
            
            # 1. N-gram blocking (most aggressive — hard block)
            if ngram_block > 0:
                logits = self._ngram_blocking(logits, generated, n=ngram_block)
                if ngram_block >= 3:
                    logits = self._ngram_blocking(logits, generated, n=4)
            
            # 2. Frequency penalty (proportional)
            logits = self._frequency_penalty(logits, generated, penalty=frequency_penalty)
            
            # 3. Presence penalty (flat diversity boost)
            logits = self._presence_penalty(logits, generated, penalty=presence_penalty)
            
            # 4. Attractor phrase blocking (narrow, speech-layer only)
            if phrase_blocking:
                logits = self._phrase_blocking(logits, generated)

            # 5. Min-length enforcement
            if i < min_tokens:
                logits[self.enc.eot_token] = -float('inf')
            
            # === SAMPLING ===
            
            # Temperature with annealing
            logits = logits / max(current_temp, 0.1)
            current_temp *= temperature_decay
            
            # Top-K filtering
            if top_k > 0:
                top_k_vals, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                threshold = top_k_vals[-1]
                logits[logits < threshold] = -float('inf')
            
            # Top-P nucleus sampling
            probs = torch.softmax(logits, dim=-1)
            sorted_probs, sorted_idx = torch.sort(probs, descending=True)
            cumulative = torch.cumsum(sorted_probs, dim=-1)
            remove = cumulative > top_p
            remove[..., 1:] = remove[..., :-1].clone()
            remove[..., 0] = False
            probs[sorted_idx[remove]] = 0.0
            
            # Normalize
            prob_sum = probs.sum()
            if prob_sum == 0 or torch.isnan(prob_sum):
                probs = torch.ones_like(probs) / self.vocab_size
            else:
                probs = probs / prob_sum
            
            next_token = torch.multinomial(probs, 1).item()
            generated.append(next_token)
            
            # EOT check (after min_tokens)
            if next_token == self.enc.eot_token and i >= min_tokens:
                break
            
            # Append new token to latent stream with correct position
            new_embed = self.embedding(
                torch.tensor([[next_token]], device=self.device)
            )
            if self.use_fp16:
                new_embed = new_embed.half()
            new_embed = new_embed.permute(1, 0, 2)
            current_latent = torch.cat([current_latent, new_embed], dim=0)
            
            # Context window management
            if current_latent.shape[0] > self.max_context:
                current_latent = current_latent[-self.max_context:, :, :]
        
        response = self.enc.decode(generated).strip()
        latency = time.perf_counter() - start
        
        # Clean up response
        response = self._clean_response(response)
        
        return {
            "response": response or "[Processing...]",
            "tokens": len(generated),
            "latency_ms": round(latency * 1000, 2),
            "domain_used": domain,
            "telemetry": {
                "karma": round(self.hpp_core.resonance_filter.karma.mean().item(), 4),
                "vairagya": round(self.hpp_core.resonance_filter.vairagya.mean().item(), 4),
                "final_temp": round(current_temp, 4),
            }
        }

    def _clean_response(self, text: str) -> str:
        """Post-process the generated text for cleanliness."""
        # Remove instruction/response markers if the model echoed them
        for marker in ["### Instruction:", "### Response:", "###"]:
            if marker in text:
                parts = text.split(marker)
                # Take the last substantial part
                text = parts[-1].strip()
        
        # Remove trailing incomplete sentences (keep last period/question/exclamation)
        last_end = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
        if last_end > len(text) * 0.3:  # Only truncate if we'd keep >30% of text
            text = text[:last_end + 1]
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @torch.no_grad()
    def nexus_pulse(self, prompt: str, auto_execute: bool = True):
        """Phase 9 NEXUS: Agency execution with upgraded inference."""
        print(f"\n[NEXUS] Processing: '{prompt}'")
        
        result = self.pulse(prompt, domain="synthesis", max_tokens=200, temperature=0.65)
        
        # Agency classification
        tokens = self.enc.encode(result['response'])
        if not tokens:
            return result
        
        token_tensor = torch.tensor([tokens], device=self.device)
        embedded = self.embedding(token_tensor)
        if self.use_fp16:
            embedded = embedded.half()
        embedded = embedded.permute(1, 0, 2)
        
        final_latent = self.university(embedded, domain="synthesis")
        
        # Back to fp32 for agency classification
        if self.use_fp16:
            final_latent = final_latent.float()
        
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
        
        if action_id != 0 and confidence > 0.50 and auto_execute:
            print(f"[NEXUS] AGENCY TRIGGERED: {action_name} ({confidence:.2%})")
            response_text = result['response']
            
            if action_name == "WRITE_FILE":
                filename = "nexus_output.txt"
                if "'" in response_text:
                    parts = response_text.split("'")
                    if len(parts) > 1:
                        filename = parts[1]
                self.toolbox.write_local_file(filename, f"HPP SYNTHESIS:\n{response_text}")
                result['agency']['executed'] = True
                
            elif action_name == "EXEC_PYTHON":
                code = response_text
                if "```python" in response_text:
                    code = response_text.split("```python")[1].split("```")[0]
                elif "```" in response_text:
                    code = response_text.split("```")[1].split("```")[0]
                self.toolbox.exec_python(code)
                result['agency']['executed'] = True
                
            elif action_name == "MASAMUNE_MOVE":
                self.toolbox.masamune_move("SECTOR_ALPHA")
                result['agency']['executed'] = True
        
        return result


# =============== TEST SUITE ===============
if __name__ == "__main__":
    engine = HPP_SovereignEngine_V2(max_context=512)
    
    print("\n" + "=" * 80)
    print("  HPP SOVEREIGN ENGINE v2.0 — SPEECH QUALITY TEST")
    print("=" * 80)
    
    prompts = [
        "Who are you?",
        "Good morning, Hepp.",
        "Explain what recursion is in simple terms.",
        "I need your help with something.",
        "Sally put the ball in the box. Anne moved it to the basket while Sally was gone. Where will Sally look for the ball?",
        "What makes you different from other AI?",
        "I'm not doing well today.",
        "Write a short reflection about what it means to grow.",
    ]
    
    for p in prompts:
        print(f"\n{'─' * 60}")
        print(f"  PROMPT: {p}")
        res = engine.pulse(p, max_tokens=120, temperature=0.78)
        try:
            print(f"  HEPP → {res['response']}")
        except UnicodeEncodeError:
            print(f"  HEPP → {res['response'].encode('ascii', 'ignore').decode('ascii')}")
        print(f"  [{res['tokens']} tokens | {res['latency_ms']}ms | domain: {res['domain_used']}]")
        print(f"  [karma: {res['telemetry']['karma']} | vairagya: {res['telemetry']['vairagya']}]")
    
    print("\n" + "=" * 80)
    print("  TEST COMPLETE")
    print("=" * 80)
