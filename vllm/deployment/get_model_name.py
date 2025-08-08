#!/usr/bin/env python3
"""
Get vLLM Model Name with Auth
Usage: python get_model_name.py [api_key]
"""
import requests
import sys

api_key = sys.argv[1] if len(sys.argv) > 1 else "some-key-there"
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get("http://localhost:6789/v1/models", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        models = response.json()
        print("Available models:")
        for model in models.get('data', []):
            model_id = model.get('id', 'unknown')
            print(f"  Model ID: {model_id}")
    else:
        print(f"Error response: {response.text}")
        
except Exception as e:
    print(f"Connection error: {e}")