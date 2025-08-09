#!/usr/bin/env python3
"""
vLLM Deployment Tester
Usage: python vllm_test_deploy.py <model_path>
Tests if a model can be loaded with vLLM before full deployment
"""
import sys
import torch
from vllm import LLM

def test_model_loading(model_path):
    try:
        print(f"Testing model loading: {model_path}")
        
        # Try loading with minimal settings
        llm = LLM(
            model=model_path,
            dtype="half",
            tensor_parallel_size=1,
            gpu_memory_utilization=0.8,
            max_model_len=2048  # Conservative for testing
        )
        
        print("✓ Model loaded successfully!")
        
        # Test generation
        outputs = llm.generate(["Hello"], max_tokens=10)
        print(f"✓ Generation test: {outputs[0].outputs[0].text}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vllm_test_deploy.py <model_path>")
        sys.exit(1)
    
    model_path = sys.argv[1]
    test_model_loading(model_path)