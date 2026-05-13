import random
import hashlib

class BACL_EntropyGenerator:
    """
    Simulates the BioAcoustic Constellation Protocol (BACL).
    In a real environment, this pulls live, localized hardware entropy (microphone data)
    to create un-spoofable hashes. For HPP, we simulate this entropy feed.
    """
    def __init__(self):
        # Simulated ambient states
        self.ambient_states = [
            "bedroom_ambient_low",
            "car_rumble_high",
            "living_room_tv",
            "backyard_wind",
            "cafe_chatter",
            "subway_screech"
        ]
        
    def generate_live_entropy(self) -> str:
        """
        Generates a simulated BACL XOR key based on 'ambient' noise.
        """
        raw_noise = f"{random.choice(self.ambient_states)}_{random.random()}"
        entropy_hash = hashlib.sha256(raw_noise.encode('utf-8')).hexdigest()[:12]
        return f"BACL_XOR_{entropy_hash.upper()}"
