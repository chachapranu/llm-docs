#!/usr/bin/env python3
"""
vLLM API Endpoint Tester
Usage: python vllm_api_test.py <base_url> <api_key>
Tests vLLM API endpoints and auth
"""
import requests
import sys

def test_vllm_api(base_url, api_key=None):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Health check: {response.status_code}")
    except:
        print("❌ Server not responding")
        return
    
    # Test 2: List models (usually doesn't need auth)
    try:
        response = requests.get(f"{base_url}/v1/models", headers=headers)
        print(f"Models endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Available models: {response.json()}")
    except Exception as e:
        print(f"Models error: {e}")
    
    # Test 3: Simple completion
    payload = {
        "prompt": "Hello",
        "max_tokens": 5
    }
    try:
        response = requests.post(f"{base_url}/v1/completions", 
                               headers=headers, json=payload)
        print(f"Completion test: {response.status_code}")
        if response.status_code != 200:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Completion error: {e}")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:6789"
    api_key = sys.argv[2] if len(sys.argv) > 2 else None
    test_vllm_api(base_url, api_key)