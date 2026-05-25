"""Speech Controller V1 — External orchestrator for HPP V2 speech."""
from __future__ import annotations

import os
import sys

import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hpp_sovereign_engine_v2 import HPP_SovereignEngine_V2
from tools.speech_loop_regression import score_response
from tools.speech_semantic_quality_review import score_item
from tools.speech_v5_language_gate import clean_sentence_metrics, leak_metrics
from tools.speech_intent_plan_gate_v1 import PROMPT_INTENT_MAP
from tools.speech_intent_plan_lite_v1 import INTENT_TOKENS


class SpeechControllerV1:
    def __init__(self, engine: HPP_SovereignEngine_V2 | None = None):
        if engine is None:
            self.engine = HPP_SovereignEngine_V2(max_context=512)
        else:
            self.engine = engine

    def classify_intent(self, prompt: str) -> str:
        """Classify the intent of the prompt using pre-defined map or fallback heuristics."""
        # 1. Exact match lookup
        if prompt in PROMPT_INTENT_MAP:
            return PROMPT_INTENT_MAP[prompt]["intent"]

        # 2. Case-insensitive lookup
        lower_prompt = prompt.lower().strip()
        for key, meta in PROMPT_INTENT_MAP.items():
            if key.lower().strip() == lower_prompt:
                return meta["intent"]

        # 3. Keyword-based heuristics
        if any(w in lower_prompt for w in ["who are you", "your name", "role", "identity", "what are you"]):
            return "identity"
        if any(w in lower_prompt for w in ["yes or no", "yes/no"]):
            return "yes/no"
        if any(w in lower_prompt for w in ["status", "state", "telemetry", "what changed"]):
            return "status"
        if any(w in lower_prompt for w in ["next step", "what is next"]):
            return "next step"
        if any(w in lower_prompt for w in ["safe", "overheat", "caution", "gpu run"]):
            return "safety"
        if any(w in lower_prompt for w in ["robot", "servo", "masamune", "hardware", "movement"]):
            return "robot/action"
        if any(w in lower_prompt for w in ["overloaded", "frustrated", "calm", "breathe", "grounded"]):
            return "emotional/protective"
        if any(w in lower_prompt for w in ["define", "what is", "explain", "leakage", "loop score"]):
            return "technical definition"

        return "status"

    def process(
        self,
        prompt: str,
        expected_target: str | None = None,
        seed: int = 14,
        prepend_intent_token: bool = True,
        use_retrieval: bool = True,
    ) -> dict:
        """Run the full Speech Controller V1 pipeline on the prompt."""
        # 1. Classify intent
        intent = self.classify_intent(prompt)

        # 2. Run HLVR retrieval to match templates
        # (Pass conversation domain for lookup to maintain maximum database match area)
        if use_retrieval:
            retrieved_final, strategy_used, similarity = self.engine.retrieve_memory(
                prompt, domain="conversation"
            )
        else:
            retrieved_final, strategy_used, similarity = None, "bypass", 0.0

        # 3. Select answer-start anchor
        retrieved_start = ""
        if retrieved_final:
            tokens = self.engine.enc.encode(retrieved_final["expected"])[:5]
            retrieved_start = self.engine.enc.decode(tokens)

        # 4. Prepend compact intent token
        token = INTENT_TOKENS.get(intent, "") if prepend_intent_token else ""
        token_prefix = f"{token} " if token else ""
        
        if retrieved_final:
            formatted_prompt = f"{token_prefix}Question: {prompt}\nAnswer: {retrieved_start}"
        else:
            formatted_prompt = f"{token_prefix}Question: {prompt}\nAnswer:"

        # Determine domain routing
        domain = "conversation"
        if intent == "identity":
            domain = "identity"
        elif intent in ["technical definition", "next step"]:
            domain = "logic"

        # 5. Call engine.pulse with bounded settings
        max_tokens = 75 if domain == "identity" else 150
        
        # Check single sentence constraints
        metadata = PROMPT_INTENT_MAP.get(prompt, {})
        max_sents = metadata.get("max_sentences", 2)
        stop_sequences = ["."] if max_sents == 1 else None

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

        response = self.engine.pulse(
            formatted_prompt,
            max_tokens=max_tokens,
            temperature=0.65,
            top_p=0.82,
            top_k=25,
            ngram_block=3,
            frequency_penalty=1.35,
            presence_penalty=0.55,
            phrase_blocking=True,
            speech_maturity_gate=True,
            speech_profile="raw",
            min_tokens=3,
            domain=domain,
            use_hlvr=False,  # Bypass internal HLVR since we orchestrate it externally
            stop_sequences=stop_sequences,
        )

        generated_text = response["response"]
        
        # 6. Reconstruct final text
        if retrieved_final:
            final_text = f"{retrieved_start} {generated_text}".strip()
        else:
            final_text = generated_text

        # 7. Apply cleanup/stop gate post-processing
        # Strip instruction markers if any leaked
        final_text = final_text.replace("Question:", "").replace("Answer:", "").strip()
        
        # Guarantee strict sentence constraints
        if max_sents == 1 and "." in final_text:
            idx = final_text.find(".")
            final_text = final_text[:idx + 1]

        # Calculate metrics
        leaks = leak_metrics(final_text)
        loop = score_response(final_text)
        sentence = clean_sentence_metrics(final_text)

        fail_reasons = []
        if leaks["format_leak_count"] > 0:
            fail_reasons.append("format_leak")
        if leaks["surface_prefix_count"] > 0:
            fail_reasons.append("surface_prefix_residue")
        if leaks["mode_label_count"] > 0:
            fail_reasons.append("mode_label_echo")
        if leaks["identity_spiral_count"] > 1:
            fail_reasons.append("identity_spiral")
        if leaks["repeated_sentence_count"] > 0:
            fail_reasons.append("repeated_sentence")
        if loop["loop_score"] > 8:
            fail_reasons.append("loop_score_high")
        if sentence["too_short"]:
            fail_reasons.append("too_short")
        if sentence["too_long"]:
            fail_reasons.append("too_long")

        surface_pass = len(fail_reasons) == 0

        semantic_pass = None
        if expected_target:
            semantic = score_item(
                {
                    "id": prompt,
                    "mode": intent,
                    "seed": seed,
                    "prompt": prompt,
                    "response": final_text,
                },
                expected_target,
            )
            semantic_pass = semantic["semantic_pass"]

        # 8. Return structured results
        return {
            "prompt": prompt,
            "intent": intent,
            "retrieval_strategy": strategy_used,
            "retrieved_prompt": retrieved_final["prompt"] if retrieved_final else None,
            "retrieval_exact_match": (retrieved_final["prompt"] == prompt) if retrieved_final else False,
            "answer_start": retrieved_start,
            "generated_text": generated_text,
            "final_text": final_text,
            "surface_pass": surface_pass,
            "semantic_pass": semantic_pass,
            "loop_score": loop["loop_score"],
            "format_leaks": leaks["format_leak_count"],
            "boundary": "retrieval_assisted_not_native_fluency",
            "telemetry": response.get("telemetry", {}),
        }
