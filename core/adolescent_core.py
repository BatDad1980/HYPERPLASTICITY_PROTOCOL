import torch
import torch.nn as nn
from .school_core import PreschoolCortex

class FrontalLobe(nn.Module):
    """
    HPP PHASE 7: THE ADOLESCENT FRONTAL LOBE
    Executive Function, Metacognition, and Fallacy Monitoring.
    
    This layer acts as a 'Second Opinion' or 'Analytical Scaffold'.
    It consumes the output of the Preschool brain and applies a 
    Multi-Head Attention mechanism to look for logical inconsistencies 
    within the generated latent thought.
    """
    def __init__(self, dim):
        super().__init__()
        # Cross-attention to monitor 'Self-Consistency'
        self.metacognitive_check = nn.MultiheadAttention(embed_dim=dim, num_heads=16)
        self.executive_gate = nn.Linear(dim * 2, dim)
        self.layer_norm = nn.LayerNorm(dim)
        
        # Hypothetical reasoning weights
        self.abstract_mapping = nn.Sequential(
            nn.Linear(dim, dim * 2),
            nn.ReLU(),
            nn.Linear(dim * 2, dim)
        )

    def forward(self, school_thought, memory_bank):
        # 1. Metacognitive reflection
        # The brain queries its own thought against the context (memory) 
        # to ensure it hasn't contradicted itself.
        reflection, _ = self.metacognitive_check(
            query=school_thought,
            key=memory_bank if memory_bank is not None else school_thought,
            value=memory_bank if memory_bank is not None else school_thought
        )
        
        # 2. Executive Gating
        # Blending the raw school output with the refined reflection
        blended = torch.cat([school_thought, reflection], dim=-1)
        executive_thought = school_thought + torch.tanh(self.executive_gate(blended))
        
        # 3. Abstract Mapping
        # Projecting into hypothetical space
        formal_thought = self.abstract_mapping(executive_thought)
        
        return self.layer_norm(formal_thought)

class AdolescentCortex(nn.Module):
    """
    HPP PHASE 7: THE ADOLESCENT ENGINE (FORMAL OPERATIONAL)
    Stacks on top of the Preschool Cortex.
    Introduces the Frontal Lobe for executive control and abstract reasoning.
    """
    def __init__(self, school_brain: PreschoolCortex, dim=512):
        super().__init__()
        self.school_brain = school_brain
        self.frontal_lobe = FrontalLobe(dim)
        
        # FREEZE the School Brain (Concrete Logic is stable)
        for param in self.school_brain.parameters():
            param.requires_grad = False
            
        # We only train the Frontal Lobe and the LM Head during Adolescence.

    def forward(self, x, current_pitch=205.0, emotion="neutral", forced_stress="LOW", memory_bank=None):
        # 1. Concrete reasoning (School Brain)
        school_thought = self.school_brain(x, current_pitch, emotion, "focus", forced_stress, memory_bank)
        
        # 2. Executive oversight (Frontal Lobe)
        adolescent_thought = self.frontal_lobe(school_thought, memory_bank)
        
        return adolescent_thought
