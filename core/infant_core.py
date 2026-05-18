import torch
import torch.nn as nn
import torch.nn.functional as F

class KarmicMicrogliaFilter(nn.Module):
    """
    Biological Microglia mapped via the Maya-Śūnyatā framework.
    Translates the 'Eat Me' (C1q/C3) and 'Don't Eat Me' (CD47) signals 
    into Karma-Weighted Pruning and Vairagya Protection.
    """
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        # Persistent state tracking for each node
        # Karma: Tracks interference/noise (Accumulated weight changes)
        self.register_buffer('karma', torch.zeros(dim))
        # Vairagya: Protection metric for stable paths
        self.register_buffer('vairagya', torch.zeros(dim))
        
        # Buddhi represents the developmental arc (0.0 = Infant, 1.0 = Mature)
        self.buddhi = 0.0

    def forward(self, x, previous_x=None):
        if previous_x is None:
            return x
            
        # 1. Calculate instant trajectory change (noise)
        trajectory_change = torch.abs(x - previous_x).mean(dim=(0, 1))
        
        # 2. Accumulate Karma (The "Eat Me" tag for noisy nodes)
        self.karma += trajectory_change
        
        # 3. Accumulate Vairagya (The "Don't Eat Me" / CD47 protection for stable, highly active nodes)
        # If the activation is high and trajectory change is low, it gains protection
        stability = (torch.abs(x).mean(dim=(0, 1)) / (trajectory_change + 1e-6))
        self.vairagya += torch.sigmoid(stability) * 0.1
        
        # 4. Calculate Survival Threshold (The Buddhi S-Curve equation)
        # As Buddhi approaches 1 (mature), the system is more conservative with pruning
        base_threshold = self.karma.mean() * 1.5
        buddhi_tensor = torch.tensor(self.buddhi - 0.5, device=self.karma.device)
        survival_threshold = base_threshold * (1.0 - torch.sigmoid(buddhi_tensor * 10))
        
        # 5. Apply Śūnyatā (Zero-Masking)
        # A node is zero-masked if its Karma exceeds the threshold AND it lacks Vairagya protection
        mask = ~((self.karma > survival_threshold) & (self.vairagya < 0.5))
        
        # Soft-gating application
        return x * mask.to(x.dtype).view(1, 1, -1)


class HyperPlasticCore(nn.Module):
    """
    HPP PHASE 1: THE INFANT ENGINE
    This isn't a static stack. This is a Recurrent Workshop designed 
    to foster 'Habit-14' logic stabilization.
    """
    def __init__(self, dim, max_loops=36):
        super().__init__()
        self.dim = dim
        self.max_loops = max_loops
        
        # The 'Master Workshop' - Shared weights for recursive reasoning
        self.workshop = nn.TransformerEncoderLayer(
            d_model=dim, 
            nhead=8, 
            dim_feedforward=dim*4,
            dropout=0.0  # ZERO DROPOUT: We don't prune during infancy.
        )
        
        # The Microglial Dampener using the Maya-Śūnyatā principles
        self.resonance_filter = KarmicMicrogliaFilter(dim)
        
        # The 'Myelin' Gates - High-speed pathways for stabilized logic
        self.myelin_sheath = nn.Linear(dim, dim)
        self.habit_tracker = 0
        self.is_stabilized = False

    def forward(self, x):
        """
        Vertical Reasoning: Instead of passing through 100 layers, 
        we loop through the Master Workshop utilizing Recurrent Depth.
        Infant Phase: Pure Sensory Auto-Encoding and Emotional Routing.
        """
        current_loops = 1 if not self.is_stabilized else self.max_loops
        
        latent_thought = x
        previous_thought = None
        
        for i in range(current_loops):
            # The recursive loop: Every pass refines the logic
            next_thought = self.workshop(latent_thought)
            
            # Apply Microglial resonance via Karma & Vairagya
            latent_thought = self.resonance_filter(next_thought, previous_thought)
            previous_thought = next_thought
            
            # Update the Buddhi (developmental arc) as loops progress
            self.resonance_filter.buddhi = min(1.0, i / 14.0)
            
            # Simulated 'Habit-14' check
            if i == 14 and not self.is_stabilized:
                self.signal_habit_lock()

        # Myelination Phase: Once stabilized, boost the signal throughput
        if self.is_stabilized:
            latent_thought = self.myelin_sheath(latent_thought)
            
        return latent_thought

    def signal_habit_lock(self):
        """
        The Architect's Protocol: Lock the logic into the permanent OS.
        """
        self.habit_tracker += 1
        if self.habit_tracker >= 14:
            print("[HPP] HABIT STABILIZED: 14 loops of resonance achieved.")
            print("[HPP] Vairagya protection locked. Initiating Synthetic Myelination...")
            self.is_stabilized = True
            # Freeze the 'Habit' so it can't be corrupted/pruned
            for param in self.workshop.parameters():
                param.requires_grad = False 
            for param in self.resonance_filter.parameters():
                param.requires_grad = False