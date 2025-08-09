#!/usr/bin/env python3
"""
Get vLLM Model Name with Auth
Usage: python get_model_name.py [api_key] [host] [port]
"""
import requests
import sys

def get_model_name(api_key="some-key-there", host="localhost", port="6789"):
    base_url = f"http://{host}:{port}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        # Test health first
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {health_response.status_code}")
        
        # Get models
        response = requests.get(f"{base_url}/v1/models", headers=headers, timeout=10)
        print(f"Models endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            print("✓ Available models:")
            for model in models.get('data', []):
                model_id = model.get('id', 'unknown')
                print(f"  Model ID: {model_id}")
                return model_id
        else:
            print(f"❌ Error response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None

if __name__ == "__main__":
    api_key = sys.argv[1] if len(sys.argv) > 1 else "some-key-there"
    host = sys.argv[2] if len(sys.argv) > 2 else "localhost"
    port = sys.argv[3] if len(sys.argv) > 3 else "6789"
    
    get_model_name(api_key, host, port)