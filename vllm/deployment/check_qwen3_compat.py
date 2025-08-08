#!/usr/bin/env python3
"""
Check Qwen3 Model Compatibility
Usage: python check_qwen3_compat.py <model_path>
"""
import sys
import os
import json

def check_model_files(model_path):
    print(f"=== Checking Qwen3 Model: {model_path} ===")
    
    # Check config files
    config_file = os.path.join(model_path, "config.json")
    if os.path.exists(config_file):
        with open(config_file) as f:
            config = json.load(f)
        print(f"Model type: {config.get('model_type', 'unknown')}")
        print(f"Architecture: {config.get('architectures', ['unknown'])}")
        print(f"Hidden size: {config.get('hidden_size', 'unknown')}")
        print(f"Vocab size: {config.get('vocab_size', 'unknown')}")
    else:
        print("❌ No config.json found")
    
    # Check tokenizer
    tokenizer_file = os.path.join(model_path, "tokenizer.json")
    print(f"Tokenizer: {'✓' if os.path.exists(tokenizer_file) else '❌'}")
    
    # Check model files
    safetensors = [f for f in os.listdir(model_path) if f.endswith('.safetensors')]
    pytorch_bins = [f for f in os.listdir(model_path) if f.endswith('.bin')]
    
    print(f"Safetensors files: {len(safetensors)}")
    print(f"PyTorch files: {len(pytorch_bins)}")
    
    return config if os.path.exists(config_file) else None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_qwen3_compat.py <model_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    check_model_files(model_path)