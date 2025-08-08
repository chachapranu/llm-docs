#!/usr/bin/env python3
"""
GPU Health Check Script
Usage: python gpu_health_check.py
Checks: GPU availability, memory, basic CUDA operations
"""
import torch
import subprocess

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