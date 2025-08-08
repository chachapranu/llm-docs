#!/usr/bin/env python3
"""
Test vLLM Tool Calling
Usage: python test_tool_calls.py
"""
import requests
import json

base_url = "http://localhost:6789"
api_key = "some-key-there"
model_id = "some-path-to-models/Qwen2.5-1.5B-Instruct"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Test with tool definition
payload = {
    "model": model_id,
    "messages": [
        {"role": "user", "content": "Calculate 15 * 24 using the calculator tool"}
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform basic arithmetic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string"},
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            }
        }
    ],
    "max_tokens": 100
}

try:
    response = requests.post(f"{base_url}/v1/chat/completions", 
                           headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✓ Tool calling response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"✗ Error: {response.text}")
except Exception as e:
    print(f"✗ Connection error: {e}")