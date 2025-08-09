#!/usr/bin/env python3
"""
Test vLLM Installation
Usage: python test_vllm_install.py
"""
def test_vllm_import():
    try:
        import vllm
        print(f"✓ vLLM import successful: {vllm.__version__}")
        
        # Test model registry
        from vllm.model_registry import _MODELS
        qwen_models = [m for m in _MODELS if 'qwen' in m.lower()]
        print(f"✓ Found {len(qwen_models)} Qwen model types")
        
        # Check for Qwen3 specifically
        qwen3_support = any('qwen3' in m.lower() for m in _MODELS)
        print(f"Qwen3 support: {'✓' if qwen3_support else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ vLLM import failed: {e}")
        return False

def test_transformers():
    try:
        import transformers
        print(f"✓ Transformers: {transformers.__version__}")
        
        # Test config import that's causing the issue
        from transformers import AutoConfig
        print("✓ AutoConfig import successful")
        return True
    except Exception as e:
        print(f"❌ Transformers error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Installation ===")
    transformers_ok = test_transformers()
    vllm_ok = test_vllm_import()
    
    if transformers_ok and vllm_ok:
        print("\n✓ All packages working!")
    else:
        print("\n❌ Package conflicts detected")