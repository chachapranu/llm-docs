# Quick LLM Deployment Reference

## Pre-Flight Checklist

```bash
# 1. Check GPU availability
python gpu_health_check.py

# 2. Calculate memory needs (replace 8 with your model size in billions)
python model_memory_calc.py 8

# 3. Clean any existing processes
python safe_cleanup.py
```

## Python Script Method (Development/Testing)

### 1. Create Config File (`quick_config.yaml`)
```yaml
single_gpu:
  model:
    path: "/path/to/your/model"           # UPDATE THIS
    dtype: "half"
    trust_remote_code: true
  deployment:
    host: "0.0.0.0"
    port: 6789
    api_key: "your-api-key"               # UPDATE THIS
  gpu:
    visible_devices: "2"                  # UPDATE THIS
    tensor_parallel_size: 1
    gpu_memory_utilization: 0.8
  performance:
    max_model_len: 4096
    block_size: 16
    swap_space: 4
  features:
    tool_call_parser: "hermes"
    log_level: "INFO"

multi_gpu:
  model:
    path: "/path/to/your/model"           # UPDATE THIS
    dtype: "half"
    trust_remote_code: true
  deployment:
    host: "0.0.0.0"
    port: 6790
    api_key: "your-api-key"               # UPDATE THIS
  gpu:
    visible_devices: "2,3"                # UPDATE THIS
    tensor_parallel_size: 2
    gpu_memory_utilization: 0.85
  performance:
    max_model_len: 2048
    block_size: 16
    swap_space: 4
  features:
    tool_call_parser: "hermes"
    log_level: "INFO"
```

### 2. Deploy Commands
```bash
# Test configuration (dry run)
python deploy_vllm.py --config quick_config.yaml --profile single_gpu --dry-run

# Deploy single GPU
python deploy_vllm.py --config quick_config.yaml --profile single_gpu

# Deploy multi-GPU
python deploy_vllm.py --config quick_config.yaml --profile multi_gpu
```

## nohup Method (Production)

### Small Models (1-3B parameters)
```bash
# Single GPU deployment
nohup CUDA_VISIBLE_DEVICES=2 vllm serve /path/to/model \
  --dtype=half \
  --tensor-parallel-size=1 \
  --port=6789 \
  --api-key=your-key \
  --tool-call-parser=hermes \
  --gpu-memory-utilization=0.9 \
  --max-model-len=8192 \
  > logs/vllm_small_$(date +%Y%m%d_%H%M%S).log 2>&1 &

echo $! > vllm_small.pid
echo "Started small model on PID: $(cat vllm_small.pid)"
```

### Medium Models (7-8B parameters)
```bash
# Option 1: Single GPU (requires 24GB+ VRAM)
nohup CUDA_VISIBLE_DEVICES=2 vllm serve /path/to/model \
  --dtype=half \
  --tensor-parallel-size=1 \
  --port=6789 \
  --api-key=your-key \
  --tool-call-parser=hermes \
  --gpu-memory-utilization=0.85 \
  --max-model-len=4096 \
  > logs/vllm_medium_single_$(date +%Y%m%d_%H%M%S).log 2>&1 &

# Option 2: Dual GPU
nohup CUDA_VISIBLE_DEVICES=2,3 vllm serve /path/to/model \
  --dtype=half \
  --tensor-parallel-size=2 \
  --port=6790 \
  --api-key=your-key \
  --tool-call-parser=hermes \
  --gpu-memory-utilization=0.9 \
  --max-model-len=4096 \
  > logs/vllm_medium_dual_$(date +%Y%m%d_%H%M%S).log 2>&1 &

echo $! > vllm_medium.pid
echo "Started medium model on PID: $(cat vllm_medium.pid)"
```

### Large Models (13B+ parameters)
```bash
# Multi-GPU required
nohup CUDA_VISIBLE_DEVICES=2,3,4,5 vllm serve /path/to/model \
  --dtype=half \
  --tensor-parallel-size=4 \
  --port=6791 \
  --api-key=your-key \
  --tool-call-parser=hermes \
  --gpu-memory-utilization=0.95 \
  --max-model-len=2048 \
  > logs/vllm_large_$(date +%Y%m%d_%H%M%S).log 2>&1 &

echo $! > vllm_large.pid
echo "Started large model on PID: $(cat vllm_large.pid)"
```

## Debug Deployments

### Conservative Settings (for troubleshooting)
```bash
nohup CUDA_VISIBLE_DEVICES=2,3 timeout 300 vllm serve /path/to/model \
  --dtype=half \
  --tensor-parallel-size=2 \
  --port=6792 \
  --api-key=your-key \
  --tool-call-parser=hermes \
  --gpu-memory-utilization=0.7 \
  --max-model-len=1024 \
  --block-size=8 \
  --swap-space=8 \
  --log-level=DEBUG \
  --enforce-eager \
  > logs/vllm_debug_$(date +%Y%m%d_%H%M%S).log 2>&1 &

echo $! > vllm_debug.pid
```

## Management Commands

### Check Status
```bash
# Check if process is running
ps -p $(cat vllm_small.pid) 2>/dev/null && echo "Running" || echo "Stopped"

# Check logs
tail -f logs/vllm_*.log

# Check API health
curl http://localhost:6789/health

# Get model name
curl -H "Authorization: Bearer your-key" http://localhost:6789/v1/models
```

### Stop Services
```bash
# Stop specific model
kill $(cat vllm_small.pid) && rm vllm_small.pid

# Stop all your vLLM processes
python stop_my_vllm.py

# Emergency cleanup
python safe_cleanup.py
```

## Quick Test Commands

### Test Deployment
```bash
# Basic completion test
curl -X POST http://localhost:6789/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-key" \
  -d '{
    "model": "your-model-path",
    "prompt": "Hello, how are you?",
    "max_tokens": 50
  }'

# Chat completion test
curl -X POST http://localhost:6789/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-key" \
  -d '{
    "model": "your-model-path", 
    "messages": [{"role": "user", "content": "What is 2+2?"}],
    "max_tokens": 20
  }'

# Tool calling test
python test_tool_calls.py
```

## One-Liner Templates

### Quick Start (copy and customize)
```bash
# UPDATE: model_path, api_key, gpu_devices
MODEL_PATH="/path/to/model"
API_KEY="your-key"
GPU_DEVICES="2,3"
PORT="6789"

# Single command deployment
nohup CUDA_VISIBLE_DEVICES=$GPU_DEVICES vllm serve $MODEL_PATH \
  --dtype=half --tensor-parallel-size=2 --port=$PORT \
  --api-key=$API_KEY --tool-call-parser=hermes \
  --gpu-memory-utilization=0.85 --max-model-len=4096 \
  > logs/vllm_$(date +%Y%m%d_%H%M%S).log 2>&1 & echo $! > vllm.pid
```

### Environment Setup
```bash
# Create logs directory
mkdir -p logs

# Set variables (customize these)
export MODEL_PATH="/path/to/your/model"
export API_KEY="your-secure-key"
export GPU_DEVICES="2,3"  # Available GPUs
export PORT="6789"
```

## Troubleshooting Quick Fixes

### Memory Issues
```bash
# Reduce memory usage
--gpu-memory-utilization=0.7 --max-model-len=1024 --block-size=8
```

### Ray Issues
```bash
# Add to command
--disable-custom-all-reduce --enforce-eager
```

### Model Loading Issues  
```bash
# Add to command
--trust-remote-code --log-level=DEBUG
```

### Can't Stop Process
```bash
# Safe stop
python stop_my_vllm.py

# If that fails
python safe_cleanup.py
```

## Best Practices

1. **Always use logs directory**: `mkdir -p logs`
2. **Save PIDs**: `echo $! > service.pid` 
3. **Use timeout for testing**: `timeout 300 vllm serve ...`
4. **Start conservative**: Low memory util, short context
5. **Test locally first**: Python script method before nohup
6. **Monitor resources**: `nvidia-smi`, `htop`