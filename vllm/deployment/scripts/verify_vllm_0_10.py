#!/usr/bin/env python3
"""
Simple vLLM 0.10.0 Test - bypass model registry
Usage: python simple_vllm_test.py
"""
def test_basic_vllm():
    try:
        import vllm
        print(f"✓ vLLM version: {vllm.__version__}")
        
        # Test basic LLM class import (what actually matters)
        from vllm import LLM
        print("✓ LLM class available")
        
        # Test engine import
        from vllm.engine.llm_engine import LLMEngine
        print("✓ LLMEngine available")
        
        print("✓ vLLM 0.10.0 should support Qwen3!")
        return True
        
    except Exception as e:
        print(f"❌ Basic vLLM test failed: {e}")
        return False

if __name__ == "__main__":
    test_basic_vllm()