#!/usr/bin/env python3
"""
Check Ray Status for vLLM
Usage: python check_ray_status.py
"""
def check_ray():
    try:
        import ray
        print(f"✓ Ray version: {ray.__version__}")
        
        # Check if Ray is running
        try:
            ray.init(address='auto', ignore_reinit_error=True)
            print("✓ Ray cluster connected")
            print(f"Ray nodes: {len(ray.nodes())}")
            ray.shutdown()
        except:
            print("❌ No existing Ray cluster")
            
    except ImportError:
        print("❌ Ray not installed")

if __name__ == "__main__":
    check_ray()