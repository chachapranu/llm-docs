# =============================================================================
# 2. model_memory_calc.py - Calculate model memory requirements
# =============================================================================
"""
Model Memory Calculator
Usage: python model_memory_calc.py <model_size_in_billions>
Calculates memory needed for model weights and typical KV cache
"""
import sys

def calculate_memory(model_size_b, precision="half", context_length=4096, batch_size=1):
    print(f"=== Memory Requirements for {model_size_b}B Model ===")
    
    # Model weights
    bytes_per_param = 2 if precision == "half" else 4
    model_memory_gb = (model_size_b * 1e9 * bytes_per_param) / (1024**3)
    print(f"Model weights ({precision}): {model_memory_gb:.1f}GB")
    
    # KV cache estimation (rough)
    # KV cache size depends on: batch_size × context_length × hidden_size × num_layers × 2 (K+V) × bytes_per_param
    # Rough estimation: ~20-40% of model size for typical context lengths
    kv_cache_ratio = min(0.4, context_length / 8192 * 0.3)  # Scale with context length
    kv_cache_gb = model_memory_gb * kv_cache_ratio * batch_size
    print(f"Estimated KV cache (ctx={context_length}, batch={batch_size}): {kv_cache_gb:.1f}GB")
    
    # Framework overhead
    overhead_gb = model_memory_gb * 0.2
    print(f"Framework overhead (~20%): {overhead_gb:.1f}GB")
    
    # Total
    total_gb = model_memory_gb + kv_cache_gb + overhead_gb
    print(f"Total estimated: {total_gb:.1f}GB")
    
    # Recommendations
    print(f"\n=== GPU Recommendations ===")
    gpu_sizes = [16, 24, 32, 40, 80]
    for gpu_size in gpu_sizes:
        utilization = total_gb / gpu_size
        if utilization <= 0.9:
            status = "✓ Fits comfortably"
        elif utilization <= 1.0:
            status = "⚠ Tight fit"
        else:
            status = "❌ Won't fit"
        print(f"{gpu_size}GB GPU: {utilization:.1f} utilization - {status}")
    
    # Tensor parallel recommendations
    print(f"\n=== Tensor Parallel Recommendations ===")
    for tp_size in [1, 2, 4, 8]:
        memory_per_gpu = total_gb / tp_size
        print(f"TP={tp_size}: {memory_per_gpu:.1f}GB per GPU")
    
    return total_gb

def main():
    if len(sys.argv) < 2:
        print("Usage: python model_memory_calc.py <model_size_in_billions> [context_length] [batch_size]")
        print("Examples:")
        print("  python model_memory_calc.py 7")
        print("  python model_memory_calc.py 8 4096 1")
        print("  python model_memory_calc.py 13 2048 4")
        sys.exit(1)
    
    model_size = float(sys.argv[1])
    context_length = int(sys.argv[2]) if len(sys.argv) > 2 else 4096
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    
    calculate_memory(model_size, "half", context_length, batch_size)

if __name__ == "__main__":
    main()