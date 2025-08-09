#!/usr/bin/env python3
"""
Test Working vLLM Deployment
Usage: python test_working_deployment.py [model_id] [api_key] [host] [port]
"""
import requests
import sys

def test_deployment(model_id=None, api_key="some-key-there", host="localhost", port="6789"):
    base_url = f"http://{host}:{port}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Get model ID if not provided
    if not model_id:
        print("Getting model ID...")
        try:
            response = requests.get(f"{base_url}/v1/models", headers=headers)
            if response.status_code == 200:
                models = response.json()
                if models.get('data'):
                    model_id = models['data'][0]['id']
                    print(f"Using model: {model_id}")
                else:
                    print("❌ No models found")
                    return
            else:
                print(f"❌ Cannot get models: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ Error getting models: {e}")
            return

    # Test completion
    print("\n=== Testing Completion Endpoint ===")
    payload = {
        "model": model_id,
        "prompt": "The capital of France is",
        "max_tokens": 10
    }

    try:
        response = requests.post(f"{base_url}/v1/completions", 
                               headers=headers, json=payload, timeout=30)
        print(f"Completion status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            text = result['choices'][0]['text']
            print(f"✓ Completion response: '{text.strip()}'")
        else:
            print(f"❌ Completion error: {response.text}")
    except Exception as e:
        print(f"❌ Completion request failed: {e}")

    # Test chat completion
    print("\n=== Testing Chat Completion Endpoint ===")
    chat_payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "max_tokens": 20
    }

    try:
        response = requests.post(f"{base_url}/v1/chat/completions", 
                               headers=headers, json=chat_payload, timeout=30)
        print(f"Chat completion status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print(f"✓ Chat response: '{message.strip()}'")
        else:
            print(f"❌ Chat error: {response.text}")
    except Exception as e:
        print(f"❌ Chat request failed: {e}")

if __name__ == "__main__":
    model_id = sys.argv[1] if len(sys.argv) > 1 else None
    api_key = sys.argv[2] if len(sys.argv) > 2 else "some-key-there"
    host = sys.argv[3] if len(sys.argv) > 3 else "localhost"
    port = sys.argv[4] if len(sys.argv) > 4 else "6789"
    
    test_deployment(model_id, api_key, host, port)