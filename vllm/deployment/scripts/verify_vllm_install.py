#!/usr/bin/env python3
"""
Verify vLLM Installation for Qwen3
Usage: python verify_vllm_install.py
"""
def test_installation():
    try:
        import vllm
        print(f"✓ vLLM version: {vllm.__version__}")
        
        # Test command line tool
        import subprocess
        result = subprocess.run(['vllm', '--help'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ vLLM CLI working")
        else:
            print(f"❌ vLLM CLI error: {result.stderr}")
            
        # Check Qwen3 support
        from vllm.model_registry import MODEL_REGISTRY
        supported_models = list(MODEL_REGISTRY.keys())
        qwen_models = [m for m in supported_models if 'qwen' in m.lower()]
        
        print(f"\n=== Qwen Model Support ===")
        for model in qwen_models:
            print(f"  ✓ {model}")
            
        qwen3_supported = any('qwen3' in m.lower() for m in supported_models)
        print(f"\nQwen3ForCausalLM support: {'✓ YES' if qwen3_supported else '❌ NO'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

if __name__ == "__main__":
    test_installation()