# 1. Test completions endpoint
curl -X POST http://localhost:6789/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer some-key-there" \
  -d '{
    "model": "your-model-name",
    "prompt": "The capital of France is",
    "max_tokens": 50,
    "temperature": 0.7
  }'

# 2. Test chat completions endpoint  
curl -X POST http://localhost:6789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer some-key-there" \
  -d '{
    "model": "your-model-name",
    "messages": [
      {"role": "user", "content": "Hello! Can you help me write a simple Python function?"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
  }'

# 3. Test streaming response
curl -X POST http://localhost:6789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer some-key-there" \
  -d '{
    "model": "your-model-name",
    "messages": [
      {"role": "user", "content": "Count from 1 to 5"}
    ],
    "max_tokens": 50,
    "stream": true
  }'

# Test server health
curl http://localhost:6789/health
# or
curl http://localhost:6789/v1/models