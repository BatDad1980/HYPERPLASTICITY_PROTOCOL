"""
HPP PHASE 14+16: THE SAMURAI BODY (KINETIC EMBODIMENT)
Translates latent thought into joint-space vectors for the Masamune chassis.

PHASE 14 (Original): Neural-to-joint mapping
PHASE 16 (Upgrade): Proprioceptive feedback loop + HAL integration
"""
import torch
import torch.nn as nn


class SamuraiBodyController(nn.Module):
    """
    HPP PHASE 14: THE SAMURAI BODY (KINETIC EMBODIMENT)
    Translates latent thought into joint-space vectors for a physical chassis.
    """
    def __init__(self, dim=512):
        super().__init__()
        self.dim = dim
        
        # 1. THE ARMS (Dual 7-DOF Manipulators)
        self.limb_map = nn.Sequential(
            nn.Linear(dim, 256),
            nn.ReLU(),
            nn.Linear(256, 14) # 7 angles per arm
        )
        
        # 2. THE STANCE (Balance and Locomotion)
        self.stance_map = nn.Sequential(
            nn.Linear(dim, 128),
            nn.ReLU(),
            nn.Linear(128, 4) # Forward/Backward, Left/Right, Rotation, Height
        )
        
        # 3. THE TOOL GRIP (Katana/Tool engagement)
        self.tool_force = nn.Linear(dim, 1) # Pressure sensor feedback
        
    def forward(self, latent_thought):
        # Extract the last state of the thought stream
        state = latent_thought[-1, :, :]
        
        limbs = torch.tanh(self.limb_map(state)) # Normalized joint angles [-1, 1]
        stance = torch.tanh(self.stance_map(state))
        grip = torch.sigmoid(self.tool_force(state)) # Grip pressure [0, 1]
        
        return {
            "left_arm": limbs[:, :7],
            "right_arm": limbs[:, 7:],
            "stance": stance,
            "grip_force": grip
        }

    def to_command_vector(self, body_output: dict) -> list:
        """
        Flatten body output dict into a single 19-element list
        for the ServoInterpolator.
        
        Returns: [left_arm(7), right_arm(7), stance(4), grip(1)]
        """
        left = body_output['left_arm'][0].tolist()
        right = body_output['right_arm'][0].tolist()
        stance = body_output['stance'][0].tolist()
        grip = [body_output['grip_force'].item()]
        return left + right + stance + grip


class KineticProprioception(nn.Module):
    """
    PHASE 16: Senses the current state of the Samurai Body.
    Encodes physical sensor readings back into the brain's latent space.
    
    This closes the perception-action loop:
    Brain → Body Controller → HAL → Servos → Sensors → Proprioception → Brain
    """
    def __init__(self, dim=512):
        super().__init__()
        # 14 (limbs) + 4 (stance) + 1 (grip) = 19 sensor inputs
        self.encoder = nn.Sequential(
            nn.Linear(19, dim),
            nn.LayerNorm(dim),
            nn.GELU(),
            nn.Linear(dim, dim)
        )
        
        # Error signal: difference between commanded and actual
        self.error_encoder = nn.Sequential(
            nn.Linear(19, dim // 2),
            nn.ReLU(),
            nn.Linear(dim // 2, dim)
        )
        
    def forward(self, body_state_vector, commanded_vector=None):
        """
        Encode physical body state into latent space for brain feedback.
        
        Args:
            body_state_vector: [Batch, 19] — actual joint positions from sensors
            commanded_vector: [Batch, 19] — what the brain commanded (optional)
            
        Returns:
            [1, Batch, Dim] — latent representation of body state, ready to 
            concatenate with the brain's thought stream
        """
        state_latent = self.encoder(body_state_vector)
        
        if commanded_vector is not None:
            # The error signal lets the brain know if the body isn't doing
            # what it asked — critical for adaptive motor control
            error = commanded_vector - body_state_vector
            error_latent = self.error_encoder(error)
            state_latent = state_latent + error_latent * 0.5
        
        # Reshape to [1, Batch, Dim] for concatenation with thought stream
        return state_latent.unsqueeze(0)
