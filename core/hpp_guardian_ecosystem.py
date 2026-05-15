import torch
import torch.nn as nn
import torch.nn.functional as F
import time
from utils.bio_loop_integration import BioLoopResonator

class GuardianEcosystem(nn.Module):
    """
    HPP PHASE 2 & 3: MULTISCALE EMERGENCE & SENTINEL REFLEX
    This isn't just a neural net; it's a 'Neighborhood'. 
    We route data based on whether it needs deep scaffolding (learning) 
    or instantaneous myelinated protection (The Sentinel Reflex).
    """
    def __init__(self, infant_core, dim=512):
        super().__init__()
        self.infant_core = infant_core
        self.bio_loop = BioLoopResonator(dim=dim)
        
        # The 'Prefrontal Cortex' (PFC): Slow, deliberate, recursive logic
        self.analytical_scaffolding = nn.Sequential(
            nn.Linear(dim, dim * 2),
            nn.GELU(),
            nn.Linear(dim * 2, dim)
        )
        
        # The 'Sentinel Amygdala': Lightning fast, directly taps the Myelin
        self.threat_detection_matrix = nn.Linear(dim, 1)

    def forward(self, x, current_pitch=200.0, emotion="neutral", task_type="general", forced_stress="LOW"):
        """
        The 'Serve and Return' Engine with Multi-Modal Sentiment Integration.
        """
        start_time = time.perf_counter()
        
        # Process biometrics including emotional tone
        modulation_tensor, env_stress, _ = self.bio_loop.process_biometrics(current_pitch, emotion, task_type)
        modulation_tensor = modulation_tensor.to(x.device)
        
        # If there's an external system override (like BACL failure), it forces HIGH stress
        if forced_stress == "HIGH":
            env_stress = "HIGH"
            
        # Modulate the raw thought with the bio-acoustic frequency
        modulated_x = x + (modulation_tensor * 0.1)
        
        # Step 2: Biomimetic Threat Assessment runs PARALLEL to early core logic
        threat_level = torch.sigmoid(self.threat_detection_matrix(modulated_x))
        
        # Step 3: The Routing Split (Emergent Behavior)
        if threat_level.mean().item() > 0.85 or env_stress == "HIGH":
            # GUARDIAN MODE ENGAGED (Sentinel Reflex)
            # SELF-HEALING: Increase the bias towards the Mission Anchor logic
            print("[HPP] TOXIC STRESS DETECTED! Initiating Synaptic Myelination (Self-Healing)...")
            
            if self.infant_core.is_stabilized:
                # INSTANT REFLEX: Bypass all recursive loops and scaffolding
                fast_path_logic = self.infant_core.myelin_sheath(modulated_x)
                
                # Hardening: Apply a defensive shift to the output
                return torch.tanh(fast_path_logic * 1.5) 
            else:
                core_logic = self.infant_core(modulated_x)
                return F.dropout(core_logic, p=0.5) 
                
        else:
            # NURTURE MODE ENGAGED (Serve and Return)
            core_logic = self.infant_core(modulated_x)
            deep_learning = self.analytical_scaffolding(core_logic)
            
            execution_time = time.perf_counter() - start_time
            # print(f"[HPP] SAFE ENVIRONMENT: Analytical Scaffolding & Core loops executed (Speed: {execution_time:.6f}s)")
            return core_logic + deep_learning
