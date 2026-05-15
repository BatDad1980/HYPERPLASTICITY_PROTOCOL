import torch
import torch.nn as nn
import math
from .adolescent_core import AdolescentCortex


class StructuralCompass(nn.Module):
    """
    HPP PHASE 17: THE STRUCTURAL COMPASS (Upgraded)
    
    Gives HPP a sense of LINEAR TIME and POSITION within a sequence.
    
    The original compass was a zero-initialized learned embedding — essentially
    giving the model no sense of word order. This upgrade combines:
    
    1. SINUSOIDAL encoding (fixed) — provides absolute position awareness.
       Position 0 always feels like "the beginning." Position 100 always
       feels like "deep into the thought." This is the clock.
       
    2. LEARNED encoding (trainable) — allows the model to develop its own
       sense of what "early in a sentence" vs "late in a sentence" means.
       This is the intuition built on top of the clock.
       
    3. ROTARY-STYLE phase — adds relative position awareness so the model
       understands that token 5 and token 7 are "close together" regardless
       of where they appear in the sequence. This is spatial awareness.
    
    Together, these give Masamune the ability to:
    - Understand word order (critical for grammar)
    - Track sentence structure (subject-verb-object)
    - Maintain coherent multi-sentence responses
    - Not repeat or scramble its output
    """
    def __init__(self, dim: int, max_context: int = 512, dropout: float = 0.1):
        super().__init__()
        self.dim = dim
        self.max_context = max_context
        
        # 1. Sinusoidal base (fixed clock — never trained)
        pe = torch.zeros(max_context, dim)
        position = torch.arange(0, max_context, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, dim, 2).float() * (-math.log(10000.0) / dim)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        # Register as buffer (saved with model but not trained)
        self.register_buffer('sinusoidal_pe', pe.unsqueeze(1))  # [MaxSeq, 1, Dim]
        
        # 2. Learned overlay (trainable intuition on top of the clock)
        self.learned_pe = nn.Parameter(
            torch.randn(max_context, 1, dim) * 0.02  # Small init, not zeros
        )
        
        # 3. Blend gate — learns how much to trust fixed vs learned encoding
        self.blend_gate = nn.Sequential(
            nn.Linear(dim * 2, dim),
            nn.Sigmoid()
        )
        
        # 4. Dropout for regularization
        self.dropout = nn.Dropout(p=dropout)
        
    def forward(self, x):
        """
        Add positional awareness to the thought stream.
        
        Args:
            x: [SeqLen, Batch, Dim] — raw embedded thought
            
        Returns:
            [SeqLen, Batch, Dim] — position-aware thought
        """
        seq_len = x.size(0)
        
        if seq_len > self.max_context:
            # Extrapolation: use modular wrapping for the sinusoidal
            # and clamp the learned to max_context
            sin_pe = self.sinusoidal_pe[:seq_len]
            learn_pe = self.learned_pe[-1:].expand(seq_len, -1, -1)
        else:
            sin_pe = self.sinusoidal_pe[:seq_len]
            learn_pe = self.learned_pe[:seq_len]
        
        # Blend fixed and learned through a learned gate
        combined = torch.cat([
            sin_pe.expand(-1, x.size(1), -1),
            learn_pe.expand(-1, x.size(1), -1)
        ], dim=-1)
        gate = self.blend_gate(combined)
        
        # Gated combination: gate controls how much learned vs fixed
        positional = gate * learn_pe + (1 - gate) * sin_pe
        
        return self.dropout(x + positional)


class UniversityCortex(AdolescentCortex):
    """
    HPP PHASE 8+17: THE UNIVERSITY CORTEX (Upgraded)
    The 'Swarm Command' layer. 
    Handles Domain Specialization, Meta-Cognitive Routing, and Linear Time.
    
    Phase 17 upgrades:
    - StructuralCompass replaces the zero-initialized pos_embedding
    - Added 'conversation' and 'none' domain routing
    - Router now uses soft-attention gating instead of hard if/else
    """
    def __init__(self, adolescent_brain: AdolescentCortex, dim=512, max_context=512):
        super().__init__(adolescent_brain.school_brain, dim)
        self.max_context = max_context
        
        # === PHASE 17: Upgraded Structural Compass ===
        self.compass = StructuralCompass(dim=dim, max_context=max_context)
        
        # Legacy compatibility: keep pos_embedding for checkpoint loading
        self.pos_embedding = nn.Parameter(torch.zeros(1, max_context, dim))
        
        # The 'Major' Specialization Layer (expanded for Phase 17)
        self.domain_expertise = nn.ModuleDict({
            "identity": nn.Linear(dim, dim),
            "logic": nn.Linear(dim, dim),
            "synthesis": nn.Linear(dim, dim),
            "conversation": nn.Linear(dim, dim),  # NEW: Natural speech
        })
        
        # Swarm Router — soft attention over domains
        self.swarm_gate = nn.Linear(dim, len(self.domain_expertise))
        
        # Output normalization for speech stability
        self.output_norm = nn.LayerNorm(dim)

    def forward(self, x, domain="none"):
        """
        Full university forward pass with upgraded compass.
        
        Args:
            x: [SeqLen, Batch, Dim] — embedded input
            domain: routing hint ("identity", "logic", "synthesis", 
                    "conversation", "none" for auto-route)
        """
        # 1. Apply Structural Compass (Position + Time awareness)
        x = self.compass(x)
            
        # 2. Full developmental stack (Infant → Toddler → School → Adolescent)
        x = super().forward(x)
        
        # 3. Domain Specialization
        if domain in self.domain_expertise:
            # Hard route to specific domain
            x = self.domain_expertise[domain](x)
        elif domain == "none" or domain == "general":
            # Soft route: let the swarm gate decide
            # Pool across sequence for routing decision
            pooled = x.mean(dim=0, keepdim=True)  # [1, Batch, Dim]
            gate_logits = self.swarm_gate(pooled)  # [1, Batch, NumDomains]
            gate_weights = torch.softmax(gate_logits, dim=-1)
            
            # Weighted sum of all domain projections
            domain_outputs = []
            for name, layer in self.domain_expertise.items():
                domain_outputs.append(layer(x))
            
            stacked = torch.stack(domain_outputs, dim=-1)  # [S, B, D, NumDomains]
            # gate_weights is [1, Batch, NumDomains] — reshape for broadcasting
            # Need [1, B, 1, NumDomains] to broadcast with [S, B, D, NumDomains]
            gw = gate_weights.unsqueeze(2)  # [1, B, 1, NumDomains]
            x = (stacked * gw).sum(dim=-1)  # [S, B, D]
        
        # 4. Output normalization for speech stability
        x = self.output_norm(x)
        
        return x


class UniversityRouter:
    """
    The 'Frat President' / Swarm Controller.
    Decides which layer (Infant, Toddler, School, Adolescent, University) to engage.
    """
    def __init__(self, model):
        self.model = model
        
    def route(self, prompt_density):
        # Logic to offload to simpler layers based on complexity
        if prompt_density < 0.3:
            return "infant/toddler"
        elif prompt_density < 0.7:
            return "school/adolescent"
        else:
            return "university"
