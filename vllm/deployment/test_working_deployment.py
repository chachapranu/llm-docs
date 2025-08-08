#!/usr/bin/env python3
"""
Test Working vLLM Deployment
Usage: python test_working_deployment.py
"""
import requests

base_url = "http://localhost:6789"
api_key = "some-key-there"
model_id = "some-path-to-models/Qwen2.5-1.5B-Instruct"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Test completion
payload = {
    "model": model_id,
    "prompt": "Hello world",
    "max_tokens": 10
}

try:
    response = requests.post(f"{base_url}/v1/completions", 
                           headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Response: {result['choices'][0]['text']}")
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Connection error: {e}")