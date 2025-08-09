# =============================================================================
# 1. gpu_health_check.py - Check GPU availability and memory
# =============================================================================
"""
GPU Health Check Script
Usage: python gpu_health_check.py
Checks: GPU availability, memory, basic CUDA operations
"""
import torch
import subprocess

def gpu_health_check():
    print("=== GPU Health Check ===")

    # Check CUDA availability
    print(f"CUDA Available: {torch.cuda.is_available()}")
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"GPU Count: {torch.cuda.device_count()}")

    # Check each GPU
    for i in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(i)
        allocated = torch.cuda.memory_allocated(i) / 1024**3
        reserved = torch.cuda.memory_reserved(i) / 1024**3
        total = props.total_memory / 1024**3
        print(f"GPU {i} ({props.name}): {allocated:.1f}GB used, {total:.1f}GB total")

    # Test basic allocation on each GPU
    print("\n=== CUDA Allocation Test ===")
    for i in range(torch.cuda.device_count()):
        try:
            torch.cuda.set_device(i)
            test_tensor = torch.zeros(1000, 1000, device=f'cuda:{i}')
            print(f"GPU {i}: ✓ Allocation OK")
            del test_tensor
        except Exception as e:
            print(f"GPU {i}: ✗ ERROR - {e}")

    # Check nvidia-smi
    print("\n=== nvidia-smi Status ===")
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=index,name,utilization.gpu,memory.used,memory.total', '--format=csv,noheader,nounits'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                parts = line.split(', ')
                if len(parts) >= 5:
                    gpu_id, name, util, mem_used, mem_total = parts[:5]
                    print(f"GPU {gpu_id}: {util}% util, {mem_used}MB/{mem_total}MB ({name})")
        else:
            print("❌ nvidia-smi failed")
    except Exception as e:
        print(f"❌ nvidia-smi error: {e}")

if __name__ == "__main__":
    gpu_health_check()