"""
HPP PHASE 16: TENSORRT EXPORT PIPELINE
Exports the HPP Sovereign Engine brain to ONNX for TensorRT compilation on Jetson.

Usage (on dev machine):
    python utils/export_tensorrt.py --export-onnx
    
Usage (on Jetson Orin NX):
    trtexec --onnx=masamune_brain.onnx --saveEngine=masamune_brain.engine --fp16

The TensorRT engine runs 10-20x faster than raw PyTorch, bringing per-token 
inference from ~150ms to ~8-15ms on the Orin NX's 1024 CUDA cores.
"""
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def export_university_to_onnx(output_path: str = "masamune_brain.onnx"):
    """
    Export the University Cortex (the main inference stack) to ONNX format.
    
    The University contains the full Infant->Toddler->School->Adolescent stack,
    so exporting it captures the entire reasoning pipeline.
    """
    import torch
    from hpp_sovereign_engine import HPP_SovereignEngine

    print("[EXPORT] Loading HPP Sovereign Engine...")
    engine = HPP_SovereignEngine(max_context=512)

    print("[EXPORT] Preparing University Cortex for ONNX trace...")
    model = engine.university
    model.eval()

    # Create dummy input matching the expected shape: [SeqLen, Batch, Dim]
    dummy_input = torch.randn(1, 1, engine.dim, device=engine.device)

    print(f"[EXPORT] Tracing with input shape: {dummy_input.shape}")
    print(f"[EXPORT] Output path: {output_path}")

    try:
        torch.onnx.export(
            model,
            (dummy_input,),
            output_path,
            input_names=["latent_thought"],
            output_names=["output_thought"],
            dynamic_axes={
                "latent_thought": {0: "seq_len"},
                "output_thought": {0: "seq_len"}
            },
            opset_version=17,
            do_constant_folding=True,
            verbose=False
        )
        print(f"[EXPORT] SUCCESS: ONNX model saved to {output_path}")
        print(f"[EXPORT] File size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
        print()
        print("[EXPORT] Next step (on Jetson Orin NX):")
        print(f"  trtexec --onnx={output_path} --saveEngine=masamune_brain.engine --fp16")

    except Exception as e:
        print(f"[EXPORT] ONNX export failed: {e}")
        print("[EXPORT] This may be due to dynamic control flow in the model.")
        print("[EXPORT] Consider using torch.jit.trace as an alternative.")
        return False

    return True


def export_body_controller_to_onnx(output_path: str = "masamune_body.onnx"):
    """
    Export the SamuraiBodyController to ONNX.
    This is a simple feedforward network — should export cleanly.
    """
    import torch
    from hpp_sovereign_engine import HPP_SovereignEngine

    print("[EXPORT] Loading SamuraiBodyController...")
    engine = HPP_SovereignEngine(max_context=512)
    model = engine.samurai_body
    model.eval()

    # Body controller expects [SeqLen, Batch, Dim]
    dummy_input = torch.randn(1, 1, engine.dim, device=engine.device)

    torch.onnx.export(
        model,
        (dummy_input,),
        output_path,
        input_names=["latent_thought"],
        output_names=["limbs", "stance", "grip"],
        opset_version=17,
        do_constant_folding=True,
        verbose=False
    )

    print(f"[EXPORT] SUCCESS: Body controller saved to {output_path}")
    print(f"[EXPORT] File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return True


def verify_onnx(model_path: str):
    """Verify an exported ONNX model is valid."""
    try:
        import onnx
        model = onnx.load(model_path)
        onnx.checker.check_model(model)
        print(f"[VERIFY] {model_path} — VALID")
        
        # Print input/output info
        for inp in model.graph.input:
            print(f"  Input:  {inp.name} {[d.dim_value for d in inp.type.tensor_type.shape.dim]}")
        for out in model.graph.output:
            print(f"  Output: {out.name} {[d.dim_value for d in out.type.tensor_type.shape.dim]}")
        return True
    except ImportError:
        print("[VERIFY] onnx package not installed. Install with: pip install onnx")
        return False
    except Exception as e:
        print(f"[VERIFY] FAILED: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HPP TensorRT Export Pipeline")
    parser.add_argument('--export-onnx', action='store_true',
                        help='Export University brain to ONNX')
    parser.add_argument('--export-body', action='store_true',
                        help='Export Body Controller to ONNX')
    parser.add_argument('--verify', type=str, default=None,
                        help='Verify an ONNX model file')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path')
    args = parser.parse_args()

    if args.verify:
        verify_onnx(args.verify)
    elif args.export_onnx:
        path = args.output or "masamune_brain.onnx"
        export_university_to_onnx(path)
    elif args.export_body:
        path = args.output or "masamune_body.onnx"
        export_body_controller_to_onnx(path)
    else:
        parser.print_help()
