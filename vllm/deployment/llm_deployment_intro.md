# LLM Deployment Fundamentals

## Core Concepts

### What is LLM Deployment?
Running a language model as a service that can handle API requests for text generation, chat, and tool calling.

### Key Components
- **Model Weights**: The actual neural network parameters (stored as `.safetensors` or `.bin` files)
- **Inference Engine**: Software that loads model and handles requests (vLLM, TGI, etc.)
- **Memory Management**: How model weights and temporary data fit in GPU/CPU memory
- **Serving Layer**: API endpoints that accept requests and return responses

## Critical Memory Math

### Model Memory Requirements
```
Base Memory = Model Parameters × Bytes per Parameter
- Half precision (fp16): 2 bytes per parameter
- Full precision (fp32): 4 bytes per parameter

Example: Qwen3-8B in half precision = 8B × 2 bytes = 16GB
```

### Total Memory Needed
```
Total = Model Weights + KV Cache + Overhead
- KV Cache: ~20-40% of model size (depends on context length)
- Overhead: ~20% for framework operations
- Safety Buffer: Always reserve 10-15% free memory

Example: Qwen3-8B total ≈ 16GB + 5GB + 3GB = 24GB
```

## Model Size Categories & Strategies

### Small Models (1-3B parameters)
**Memory**: 2-6GB | **Strategy**: Single GPU
```bash
# Example: Qwen2.5-1.5B
CUDA_VISIBLE_DEVICES=0 vllm serve model_path \
  --dtype=half \
  --gpu-memory-utilization=0.9 \
  --max-model-len=8192
```
**Key Considerations**:
- Can use high memory utilization (90%+)
- Support longer contexts
- Single GPU deployment is sufficient

### Medium Models (7-8B parameters)
**Memory**: 14-20GB | **Strategy**: Single high-memory GPU or 2 GPUs
```bash
# Single GPU (needs 24GB+ VRAM)
CUDA_VISIBLE_DEVICES=0 vllm serve model_path \
  --dtype=half \
  --gpu-memory-utilization=0.85 \
  --max-model-len=4096

# Dual GPU (tensor parallelism)
CUDA_VISIBLE_DEVICES=0,1 vllm serve model_path \
  --dtype=half \
  --tensor-parallel-size=2 \
  --gpu-memory-utilization=0.9
```
**Key Considerations**:
- Reduce context length if memory constrained
- Consider tensor parallelism for better performance
- Monitor memory usage carefully

### Large Models (13B+ parameters)
**Memory**: 26GB+ | **Strategy**: Multi-GPU required
```bash
# 4-GPU setup for 13B+ models
CUDA_VISIBLE_DEVICES=0,1,2,3 vllm serve model_path \
  --dtype=half \
  --tensor-parallel-size=4 \
  --gpu-memory-utilization=0.95 \
  --max-model-len=2048
```
**Key Considerations**:
- Tensor parallelism is mandatory
- Shorter context lengths
- Higher memory utilization possible
- Network bandwidth between GPUs matters

## Tensor Parallelism Basics

### When to Use
- **Single GPU**: Model fits comfortably with room for KV cache
- **Multi-GPU**: Model + KV cache exceeds single GPU memory

### How It Works
```
Model layers split across GPUs:
- GPU 0: Layers 0-7
- GPU 1: Layers 8-15
- GPU 2: Layers 16-23
- GPU 3: Layers 24-31
```

### Performance Impact
- **Benefit**: Enables large model deployment
- **Cost**: Inter-GPU communication overhead
- **Rule**: Use minimum GPUs needed for memory

## Quick Decision Framework

### 1. Calculate Memory Needs
```python
model_gb = parameters_billions * 2  # half precision
total_needed = model_gb * 1.4  # with KV cache + overhead
```

### 2. Choose Strategy
```
if total_needed <= single_gpu_memory * 0.9:
    use_single_gpu()
elif total_needed <= dual_gpu_memory * 0.9:
    use_tensor_parallel_2()
else:
    use_tensor_parallel_4_plus()
```

### 3. Set Parameters
```python
# Conservative (safe)
gpu_memory_utilization = 0.8
max_model_len = 2048

# Aggressive (max performance)
gpu_memory_utilization = 0.95
max_model_len = 8192
```

## Common Deployment Patterns

### Development/Testing
```bash
# Fast startup, minimal resource usage
vllm serve model --dtype=half --max-model-len=1024 --gpu-memory-utilization=0.7
```

### Production
```bash
# Optimized for throughput
vllm serve model --dtype=half --max-model-len=4096 --gpu-memory-utilization=0.9 \
  --tensor-parallel-size=2 --block-size=32
```

### Debugging
```bash
# Verbose logging, conservative settings
vllm serve model --dtype=half --max-model-len=512 --gpu-memory-utilization=0.6 \
  --log-level=DEBUG --enforce-eager
```

## Key Takeaways

1. **Memory is the primary constraint** - calculate before deploying
2. **Start conservative** - increase utilization after confirming stability  
3. **Context length trades with batch size** - shorter contexts = more concurrent users
4. **Tensor parallelism adds complexity** - use only when necessary
5. **Monitor resource usage** - GPU memory, CPU, network I/O