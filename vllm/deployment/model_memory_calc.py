#!/usr/bin/env python3
"""
Model Memory Calculator
Usage: python model_memory_calc.py <model_size_in_billions>
Calculates memory needed for model weights and typical KV cache
"""
import sys

def calculate_memory(model_size_b, precision="half"):
    bytes_per_param = 2 if precision == "half" else 4
    
    # Model weights
    model_memory_gb = (model_size_b * 1e9 * bytes_per_param) / (1024**3)
    
    # Typical KV cache (rough estimate for 4k context)
    kv_cache_gb = model_memory_gb * 0.3  # ~30% of model size
    
    # Total with overhead
    total_gb = model_memory_gb * 1.4  # 40% overhead for safety
    
    print(f"=== Memory Requirements for {model_size_b}B Model ===")
    print(f"Model weights ({precision}): {model_memory_gb:.1f}GB")
    print(f"Estimated KV cache: {kv_cache_gb:.1f}GB")
    print(f"Total recommended: {total_gb:.1f}GB")
    
    return total_gb

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python model_memory_calc.py <model_size_in_billions>")
        sys.exit(1)
    
    size = float(sys.argv[1])
    calculate_memory(size)