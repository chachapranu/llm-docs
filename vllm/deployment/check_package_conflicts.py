#!/usr/bin/env python3
"""
Check for package conflicts affecting vLLM
Usage: python check_package_conflicts.py
"""
import sys
import subprocess

def check_package_versions():
    packages = ['vllm', 'transformers', 'torch', 'accelerate', 'tokenizers']
    
    print("=== Package Versions ===")
    for pkg in packages:
        try:
            result = subprocess.run([sys.executable, '-c', f'import {pkg}; print({pkg}.__version__)'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{pkg}: {result.stdout.strip()}")
            else:
                print(f"{pkg}: ❌ Not installed or error")
        except:
            print(f"{pkg}: ❌ Import error")

def check_transformers_config():
    try:
        from transformers import AutoConfig
        print("\n=== Transformers Config Check ===")
        print("✓ Transformers config import successful")
    except Exception as e:
        print(f"❌ Transformers config error: {e}")

if __name__ == "__main__":
    check_package_versions()
    check_transformers_config()