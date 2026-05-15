import torch
import torch.nn as nn
from .toddler_core import ToddlerCortex

class Hippocampus(nn.Module):
    """
    The Preschooler's Memory Bank.
    Implements a Neural Turing Machine-style cross-attention read head.
    It allows the AI to pause, query its past context (or an external vector database), 
    and inject that memory into its current thought before speaking.
    """
    def __init__(self, dim):
        super().__init__()
        # Using Seq-First (default) to match the Infant & Toddler architectures
        self.memory_attention = nn.MultiheadAttention(embed_dim=dim, num_heads=8)
        self.layer_norm = nn.LayerNorm(dim)
        self.memory_gate = nn.Linear(dim * 2, dim)

    def forward(self, current_thought, memory_bank):
        # If there is no memory yet, return the thought unchanged
        if memory_bank is None or memory_bank.size(0) == 0:
            return current_thought
            
        # Query the memory bank using the current thought
        # current_thought: [Seq, Batch, Dim]
        # memory_bank: [MemSeq, Batch, Dim]
        recalled_memory, _ = self.memory_attention(
            query=current_thought, 
            key=memory_bank, 
            value=memory_bank
        )
        
        # Gate the memory (decide how much of the memory to blend)
        blended = torch.cat([current_thought, recalled_memory], dim=-1)
        gated_thought = current_thought + torch.tanh(self.memory_gate(blended))
        
        return self.layer_norm(gated_thought)

class PreschoolCortex(nn.Module):
    """
    HPP PHASE 5: THE PRESCHOOL ENGINE
    Stacks on top of the Toddler Cortex.
    Introduces the Hippocampus for concrete operational memory and factual retrieval.
    """
    def __init__(self, toddler_brain: ToddlerCortex, dim=512):
        super().__init__()
        self.toddler_brain = toddler_brain
        self.hippocampus = Hippocampus(dim)
        
        # We freeze the Infant (Perception)
        for param in self.toddler_brain.infant_ecosystem.parameters():
            param.requires_grad = False
            
        # We DO NOT freeze the Toddler's Broca's Area entirely, because Preschool is 
        # still a critical period for language acquisition (TinyStories).
        # We allow a small learning rate to continue refining it, but the main focus
        # is training the Hippocampus to retrieve facts.

    def forward(self, x, current_pitch=200.0, emotion="neutral", task_type="general", forced_stress="LOW", memory_bank=None):
        # 1. Infant perceives and routes
        infant_thought = self.toddler_brain.infant_ecosystem(x, current_pitch, emotion, task_type, forced_stress)
        
        # 2. Hippocampus retrieves relevant context based on the Infant's raw perception
        remembered_thought = self.hippocampus(infant_thought, memory_bank)
        
        # 3. Toddler formulates the speech using the memory-augmented thought
        final_thought = self.toddler_brain.broca(remembered_thought)
        
        return final_thought
