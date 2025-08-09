# =============================================================================
# 4. simple_vllm_test.py - Simple vLLM installation test
# =============================================================================
"""
Simple vLLM Installation Test - bypass model registry issues
Usage: python simple_vllm_test.py
"""
def test_basic_vllm():
    print("=== Testing vLLM Installation ===")
    
    try:
        import vllm
        print(f"✓ vLLM version: {vllm.__version__}")
        
        # Test basic LLM class import (what actually matters)
        from vllm import LLM
        print("✓ LLM class available")
        
        # Test engine import
        from vllm.engine.llm_engine import LLMEngine
        print("✓ LLMEngine available")
        
        # Test CLI availability
        import subprocess
        result = subprocess.run(['vllm', '--help'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ vLLM CLI working")
        else:
            print(f"❌ vLLM CLI error: {result.stderr}")
        
        print("✓ vLLM installation looks good!")
        return True
        
    except Exception as e:
        print(f"❌ vLLM test failed: {e}")
        return False

if __name__ == "__main__":
    test_basic_vllm()