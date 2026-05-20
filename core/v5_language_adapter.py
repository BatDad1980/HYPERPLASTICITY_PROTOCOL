"""Diagnostic language adapter wrapper for HPP V2 speech.

This adapter packages bounded inference behavior for measurement only:
stable speech profile, bounded token count, and explicit checkpoint loading.
It is not a V5-native import and does not imply promotion.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2


DEFAULT_CHECKPOINT = os.path.join("checkpoints", "hpp_speech_identity_containment_v1.pth")


@dataclass(frozen=True)
class V5LanguageAdapterConfig:
    checkpoint: str = DEFAULT_CHECKPOINT
    power_mode: str = "plugged"
    max_context: int = 512
    max_tokens: int = 56
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    min_tokens: int = 8


class V5SafeLanguageAdapter:
    """Thin diagnostic inference wrapper around HPP V2 speech."""

    def __init__(self, config: V5LanguageAdapterConfig | None = None) -> None:
        self.config = config or V5LanguageAdapterConfig()
        self.engine = HPP_SovereignEngine_V2(max_context=self.config.max_context)
        self._load_checkpoint(self.config.checkpoint)
        self.engine.set_power_mode(self.config.power_mode)

    def answer(self, prompt: str, *, seed: int | None = None, mode: str = "conversation") -> dict:
        if seed is not None:
            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)

        result = self.engine.pulse(
            prompt,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            top_k=self.config.top_k,
            ngram_block=3,
            frequency_penalty=1.25,
            presence_penalty=0.45,
            speech_profile="stable",
            min_tokens=self.config.min_tokens,
            domain=mode,
        )
        result["adapter"] = "v5_safe_language_adapter"
        result["checkpoint"] = self.config.checkpoint
        result["speech_profile"] = "stable"
        return result

    def _load_checkpoint(self, checkpoint_path: str) -> None:
        checkpoint = torch.load(checkpoint_path, map_location=self.engine.device, weights_only=True)
        self.engine.university.load_state_dict(checkpoint.get("masamune_state_dict", {}), strict=False)
        if "lm_head_state_dict" in checkpoint:
            self.engine.lm_head.load_state_dict(checkpoint["lm_head_state_dict"])
        if "embedding_state_dict" in checkpoint:
            self.engine.embedding.load_state_dict(checkpoint["embedding_state_dict"])
        if self.engine.use_fp16:
            self.engine.university.half()
            self.engine.lm_head.half()
            self.engine.embedding.half()
        self.engine.eval_mode()
