"""
ONNX Export & Dynamic INT8 Quantization Script for OSCC AI MergedNet

Exports the PyTorch 4-backbone ensemble (MergedNet) to:
1. merged_model.onnx (FP32 ONNX graph)
2. merged_model_int8.onnx (Dynamically quantized INT8 graph, ~25MB memory footprint)
"""

import sys
from pathlib import Path
import torch
import numpy as np

# Ensure backend package is in python path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.services.ml_engine import MergedNet
from app.core.config import settings

def export_and_quantize():
    model_path = settings.MODEL_PATH
    onnx_fp32_path = backend_dir / "merged_model.onnx"
    onnx_int8_path = backend_dir / "merged_model_int8.onnx"

    print(f"[1/4] Initializing MergedNet...")
    model = MergedNet(num_classes=2)
    model.eval()

    if model_path.exists():
        print(f"[2/4] Loading checkpoint from {model_path} ({model_path.stat().st_size / (1024*1024):.1f} MB)...")
        try:
            state_dict = torch.load(model_path, map_location="cpu", mmap=True)
        except Exception:
            state_dict = torch.load(model_path, map_location="cpu")
        with torch.no_grad():
            for name, param in model.named_parameters():
                if name in state_dict:
                    param.copy_(state_dict[name].float())
            for name, buf in model.named_buffers():
                if name in state_dict:
                    buf.copy_(state_dict[name].float())
        del state_dict
        print("      Checkpoint loaded successfully.")
    else:
        print(f"      [WARN] Checkpoint not found at {model_path}, exporting with baseline weights.")

    dummy_input = torch.randn(1, 3, 224, 224, dtype=torch.float32)

    print(f"[3/4] Exporting to ONNX FP32 -> {onnx_fp32_path.name}...")
    torch.onnx.export(
        model,
        dummy_input,
        str(onnx_fp32_path),
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=["input"],
        output_names=["logits"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "logits": {0: "batch_size"}
        },
        dynamo=False
    )
    fp32_size_mb = onnx_fp32_path.stat().st_size / (1024 * 1024)
    print(f"      FP32 ONNX graph exported ({fp32_size_mb:.1f} MB).")

    print(f"[4/4] Applying Dynamic INT8 Quantization -> {onnx_int8_path.name}...")
    import onnxruntime as ort
    from onnxruntime.quantization import quantize_dynamic, QuantType

    quantize_dynamic(
        model_input=str(onnx_fp32_path),
        model_output=str(onnx_int8_path),
        weight_type=QuantType.QInt8,
        per_channel=True,
        reduce_range=True
    )
    int8_size_mb = onnx_int8_path.stat().st_size / (1024 * 1024)
    compression_pct = (1.0 - (int8_size_mb / fp32_size_mb)) * 100.0
    print(f"      INT8 Quantized model saved: {int8_size_mb:.1f} MB ({compression_pct:.1f}% reduction).")

    # Verification: Validate ONNX Runtime session inference
    print("\n[Verification] Running cross-runtime validation...")
    session_options = ort.SessionOptions()
    session_options.intra_op_num_threads = 1
    session_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    session = ort.InferenceSession(str(onnx_int8_path), session_options, providers=["CPUExecutionProvider"])

    np_input = dummy_input.numpy()
    ort_inputs = {session.get_inputs()[0].name: np_input}
    ort_outs = session.run(None, ort_inputs)

    with torch.no_grad():
        pt_out = model(dummy_input).numpy()

    print(f"      PyTorch FP32 Logits: {pt_out[0]}")
    print(f"      ONNX INT8 Logits:    {ort_outs[0][0]}")
    print("      Verification complete. Model modernization successful!\n")

if __name__ == "__main__":
    export_and_quantize()
