# LLM Deployment Debugging Guide

## Systematic Debugging Approach

### 1. Identify the Failure Stage
```
Model Loading → KV Cache Allocation → Server Start → First Request → Runtime
```

### 2. Error Categories & Solutions

## Memory-Related Errors

### Symptoms
- `CUDA out of memory`
- `torch.zeros CUDA error invalid argument`
- Process killed without error message

### Diagnostic Scripts
```bash
# Check GPU memory
python gpu_health_check.py

# Calculate model requirements  
python model_memory_calc.py 8  # for 8B model
```

### Solutions (in order)
1. **Reduce memory utilization**: `--gpu-memory-utilization=0.8`
2. **Shorter context**: `--max-model-len=2048`
3. **Smaller blocks**: `--block-size=8`
4. **Add tensor parallelism**: `--tensor-parallel-size=2`
5. **CPU offloading**: `--cpu-offload-gb=4`

## Ray/Distributed Errors

### Symptoms
- "Ray cluster not initialized"
- Process hangs at "Starting Ray"
- "Ray worker timeout"

### Immediate Action
```bash
# Don't use Ctrl+C! Open new terminal:
python stop_my_vllm.py

# Clean up
python safe_cleanup.py
```

### Prevention
- Use `timeout 300` for deployments
- Single GPU first, then scale up
- Check existing Ray processes before starting

## Model Loading Errors

### Symptoms
- `No module named 'vllm.model_registry'`
- `Unsupported model architecture`
- `Config.json not found`

### Diagnostics
```bash
# Check vLLM installation
python simple_vllm_test.py

# Verify model files
python check_qwen3_compat.py /path/to/model

# Test model loading
python vllm_test_deploy.py /path/to/model
```

### Solutions
1. **Update vLLM**: `pip install vllm --upgrade`
2. **Add trust flag**: `--trust-remote-code`
3. **Force architecture**: `--model-loader-extra-config`

## API/Authentication Errors

### Symptoms
- `401 Unauthorized`
- `400 Bad Request`
- `Connection refused`

### Debug Process
```bash
# 1. Check server status
curl http://localhost:6789/health

# 2. Test without auth
curl http://localhost:6789/v1/models

# 3. Get model name
python get_model_name.py your-api-key

# 4. Test with correct model ID
python test_working_deployment.py
```

## Shared Server Issues

### GPU Conflicts
```bash
# Check what's running
python check_gpu_usage.py

# Use different GPUs
CUDA_VISIBLE_DEVICES=2,3  # avoid busy GPUs
```

### Process Cleanup
```bash
# Safe cleanup (only your processes)
python safe_cleanup.py

# Check remaining processes  
ps -u $USER | grep -E "(ray|vllm)"
```

## Performance Issues

### Slow Startup
- **Cause**: Large model loading, Ray initialization
- **Solution**: Use `--log-level=DEBUG` to see progress
- **Timeout**: Always use `timeout 300` command

### Slow Inference
- **Check**: GPU utilization with `nvidia-smi`
- **Optimize**: Increase `--gpu-memory-utilization`
- **Scale**: Add `--tensor-parallel-size`

## Tool Calling Issues

### Parser Errors
```bash
# Wrong: --tool-call-parse hermes
# Correct: --tool-call-parser hermes
```

### Testing Tool Calls
```bash
python test_tool_calls.py  # Use provided script
```

## Quick Reference: When to Use Each Script

### Pre-Deployment
- `gpu_health_check.py` - Verify GPU availability
- `model_memory_calc.py` - Calculate memory needs
- `check_qwen3_compat.py` - Verify model format

### During Issues
- `safe_cleanup.py` - Clean up processes safely
- `stop_my_vllm.py` - Stop hung deployments
- `simple_vllm_test.py` - Test vLLM installation

### Post-Deployment Testing
- `get_model_name.py` - Get correct model ID
- `test_working_deployment.py` - Test basic API
- `test_tool_calls.py` - Test tool calling

### Monitoring
- `check_gpu_usage.py` - Monitor shared server
- `check_ray_status.py` - Debug Ray issues

## Emergency Procedures

### Completely Stuck Process
1. **Never force kill on shared server**
2. Use `python stop_my_vllm.py` first
3. If that fails: single `Ctrl+C` then immediate cleanup
4. Run `python safe_cleanup.py`

### Can't Connect to API
1. Check if server is actually running: `curl localhost:6789/health`
2. Verify model name: `python get_model_name.py`
3. Test with correct model ID in requests

### Out of Memory on Multi-GPU
1. Reduce to single GPU first
2. Lower `--gpu-memory-utilization`
3. Decrease `--max-model-len`
4. Add `--cpu-offload-gb`

## Best Practices

### Always Start With
```bash
# Conservative test deployment
CUDA_VISIBLE_DEVICES=2 timeout 120 vllm serve model_path \
  --dtype=half --tensor-parallel-size=1 \
  --gpu-memory-utilization=0.7 --max-model-len=1024 \
  --log-level=DEBUG
```

### Scale Up Gradually
1. Single GPU → Multi-GPU
2. Low memory util → High memory util  
3. Short context → Long context
4. DEBUG logging → INFO logging

### Monitor Continuously
- GPU memory usage
- Server logs
- API response times
- Other users' processes (shared server)