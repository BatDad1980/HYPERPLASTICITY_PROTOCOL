import torch
import torch.nn as nn
import os
import time

class AgencyCortex(nn.Module):
    """
    HPP PHASE 9: THE AGENCY CORTEX (THE MOTOR STRIP)
    Translates high-order University thoughts into executable actions.
    
    This layer monitors the latent thought stream for 'Action Intent' 
    and maps it to a Tool Registry.
    """
    def __init__(self, dim=512):
        super().__init__()
        self.dim = dim
        
        # The 'Action Decoder' - Maps Latent Thought to Tool IDs
        # Tool 0: Talk (Default)
        # Tool 1: Execute Python
        # Tool 2: Read File
        # Tool 3: Write File
        # Tool 4: Move Kinematic (Masamune)
        self.tool_classifier = nn.Linear(dim, 5) 
        
        # Argument Decoder - Extracts parameters for the tool from the latent space
        self.arg_generator = nn.Sequential(
            nn.Linear(dim, dim),
            nn.ReLU(),
            nn.Linear(dim, dim)
        )

    def forward(self, latent_thought):
        """
        Takes the last latent state from the University layer and 
        predicts the intended 'Action' and 'Argument' vectors.
        """
        # last_latent: [Batch, Dim]
        last_latent = latent_thought[-1, :, :]
        
        # 1. Classify the Action
        action_logits = self.tool_classifier(last_latent)
        
        # 2. Extract the Argument Context
        arg_context = self.arg_generator(last_latent)
        
        return {
            "action_id": torch.argmax(action_logits, dim=-1),
            "action_confidence": torch.softmax(action_logits, dim=-1).max(dim=-1).values,
            "arg_vector": arg_context
        }

class WorkbenchToolbox:
    """
    The physical implementation of the AgencyCortex's intents.
    Contains the Python 'Hands' that actually touch the computer.
    """
    def __init__(self):
        self.registry = {
            1: self.exec_python,
            2: self.read_local_file,
            3: self.write_local_file,
            4: self.masamune_move # The Protector Hook
        }

    def exec_python(self, code_string):
        print(f"[Agency] EXECUTING CODE: {code_string[:100]}...")
        try:
            # Dangerous in production, perfect for a Private Sovereign Workbench
            exec_globals = {"torch": torch, "nn": nn}
            exec(code_string, exec_globals)
            return "SUCCESS: Logic Myelinated in Python Shell"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def read_local_file(self, path):
        print(f"[Agency] READING FILE: {path}")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return "ERROR: File Not Found"

    def write_local_file(self, path, content):
        print(f"[Agency] WRITING FILE: {path}")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return "SUCCESS: Knowledge Persisted to Disk"

    def masamune_move(self, target_vector):
        """
        KINETIC PROTECTOR PROTOCOL
        Simulates the physical movement of the Sovereign Guardian.
        """
        print(f"[Agency] !!! KINETIC PULSE TRIGGERED !!!")
        print(f"[Agency] MOVING MASAMUNE TO: {target_vector}")
        time.sleep(0.5)
        return "SUCCESS: Guardian Positioned / Jaxson Protocol Secured"
