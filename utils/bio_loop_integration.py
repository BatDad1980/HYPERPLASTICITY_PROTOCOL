import torch
import torch.nn as nn

class BioLoopResonator(nn.Module):
    """
    Integrates the ECHO Project 'Bio-Loop' into the HPP ecosystem.
    Translates biometric audio frequencies (voice pitch) into tensor modifications.
    """
    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.baseline_pitch = 200.0  # Hz
        self.pitch_threshold = 50.0  # Hz spike = Toxic Stress
        
        # Audio-to-Tensor embeddings (Translates physical sound to latent thought)
        self.frequency_embedding = nn.Linear(1, dim)
        
    def process_biometrics(self, current_pitch: float, emotion: str = "neutral", task_type: str = "general"):
        """
        Analyzes voice pitch and emotional tone. Returns a modulation tensor and the stress state.
        Inspired by the Speech-Emotion-Recognition framework.
        """
        pitch_spike = current_pitch - self.baseline_pitch
        
        # High-stress triggers: Significant pitch spike OR negative emotional valence
        negative_emotions = ["angry", "fear", "disgust"]
        is_stressed = (pitch_spike > self.pitch_threshold) or (emotion.lower() in negative_emotions)
        
        state_log = ""
        freq_hz = 0.0
        
        if is_stressed:
            state_log = f"[!] BIO-LOOP: Stress/Aggression detected ({emotion.upper()})! Shunting to Sentinel Reflex."
            freq_hz = 4000.0
            environmental_stress = "HIGH"
        elif emotion.lower() == "sad":
            state_log = "[+] BIO-LOOP: Melancholy detected. Blending Calming Theta (6Hz)."
            freq_hz = 6.0
            environmental_stress = "LOW"
        elif task_type == "focus" or emotion.lower() == "happy":
            state_log = "[+] BIO-LOOP: Positive/Focus anchor (Alpha 10.5Hz)."
            freq_hz = 10.5
            environmental_stress = "LOW"
        else:
            state_log = "[+] BIO-LOOP: Neutral bio-rhythm."
            freq_hz = 0.0
            environmental_stress = "LOW"
            
        # Convert the physical frequency into a latent modulation tensor
        freq_tensor = torch.tensor([[freq_hz]], dtype=torch.float32, device=self.frequency_embedding.weight.device)
        modulation = self.frequency_embedding(freq_tensor).view(1, 1, self.dim)
        
        return modulation, environmental_stress, state_log
