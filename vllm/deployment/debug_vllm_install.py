#!/usr/bin/env python3
"""
Debug vLLM Installation Issues
Usage: python debug_vllm_install.py
"""
import sys
import subprocess
import importlib.util

def check_vllm_package():
    print("=== vLLM Package Debug ===")
    
    # Check if vLLM package exists
    spec = importlib.util.find_spec("vllm")
    if spec is None:
        print("❌ vLLM package not found")
        return False
    else:
        print(f"✓ vLLM package found at: {spec.origin}")
    
    # Try importing vLLM
    try:
        import vllm
        print(f"✓ vLLM import successful")
        print(f"✓ vLLM version: {vllm.__version__}")
        return True
    except Exception as e:
        print(f"❌ vLLM import failed: {e}")
        return False

def check_vllm_cli():
    print("\n=== vLLM CLI Debug ===")
    
    # Check if vllm command exists
    try:
        result = subprocess.run(['which', 'vllm'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ vLLM CLI found at: {result.stdout.strip()}")
        else:
            print("❌ vLLM CLI not in PATH")
    except:
        print("❌ Cannot check vLLM CLI location")
    
    # Try running vllm command with error details
    try:
        result = subprocess.run(['vllm', '--version'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✓ vLLM CLI working: {result.stdout}")
        else:
            print(f"❌ vLLM CLI error (stderr): {result.stderr}")
            print(f"❌ vLLM CLI error (stdout): {result.stdout}")
    except subprocess.TimeoutExpired:
        print("❌ vLLM CLI command timed out")
    except Exception as e:
        print(f"❌ vLLM CLI error: {e}")

def check_python_path():
    print(f"\n=== Python Environment ===")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check pip list for vllm
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
        vllm_lines = [line for line in result.stdout.split('\n') if 'vllm' in line.lower()]
        if vllm_lines:
            print("✓ vLLM in pip list:")
            for line in vllm_lines:
                print(f"  {line}")
        else:
            print("❌ vLLM not found in pip list")
    except Exception as e:
        print(f"❌ Cannot check pip list: {e}")

if __name__ == "__main__":
    check_python_path()
    package_ok = check_vllm_package()
    check_vllm_cli()