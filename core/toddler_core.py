import torch
import torch.nn as nn
from .hpp_guardian_ecosystem import GuardianEcosystem

class BrocasArea(nn.Module):
    """
    The Toddler's Speech Center. 
    Takes the emotionally-routed, myelinated latent thought from the Infant,
    and applies Auto-Regressive sequence prediction (Language generation).
    """
    def __init__(self, dim):
        super().__init__()
        # A causal workshop specifically for generating speech sequences
        self.speech_layer = nn.TransformerEncoderLayer(
            d_model=dim, 
            nhead=8, 
            dim_feedforward=dim*4,
            dropout=0.1
        )
        self.layer_norm = nn.LayerNorm(dim)

    def forward(self, x):
        # Generate causal mask for the speech center
        seq_len = x.size(0)
        causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len, device=x.device)
        
        # Apply causal masking to prevent looking into the future
        speech_thought = self.speech_layer(x, src_mask=causal_mask)
        return self.layer_norm(speech_thought)

class ToddlerCortex(nn.Module):
    """
    HPP PHASE 4: THE TODDLER ENGINE
    Works IN CONJUNCTION with the Infant. 
    Infant handles Perception & Reflexes (GuardianEcosystem).
    Toddler handles Articulation & Auto-Regressive Prediction (BrocasArea).
    """
    def __init__(self, infant_ecosystem: GuardianEcosystem, dim=512):
        super().__init__()
        self.infant_ecosystem = infant_ecosystem
        self.broca = BrocasArea(dim)
        
        # We freeze the Infant's physical brain weights so the Toddler builds ON TOP of them,
        # without destroying the Infant's fundamental perceptions.
        for param in self.infant_ecosystem.parameters():
            param.requires_grad = False

    def forward(self, x, current_pitch=200.0, emotion="neutral", task_type="general", forced_stress="LOW"):
        # 1. The Infant perceives the world and routes it (Reflex vs Analytical)
        # Note: To prevent data leakage during causal prediction, we can pass a causal mask to the infant.
        # But for now, we rely on the Toddler's Broca's area to enforce causality on the extracted features.
        infant_thought = self.infant_ecosystem(x, current_pitch, emotion, task_type, forced_stress)
        
        # 2. The Toddler attempts to formulate a response/prediction
        toddler_thought = self.broca(infant_thought)
        
        return toddler_thought
