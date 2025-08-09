# LLM Deployment Terminology Guide

## Core Model Concepts

### Model Architecture
**What**: The neural network structure (transformer layers, attention heads, hidden dimensions)
**Example**: `Qwen3ForCausalLM`, `LlamaForCausalLM`
**Importance**: Determines memory needs, compatibility with inference engines
**Practical**: Check `config.json` for `"architectures"` field

### Model Parameters
**What**: Total number of trainable weights in the neural network
**Example**: 8B = 8 billion parameters
**Importance**: Directly affects memory requirements (8B × 2 bytes = 16GB in half precision)
**Practical**: Bigger models = better performance but more resources needed

### Precision/Data Type (dtype)
**What**: Number format for storing model weights
- `half/fp16`: 2 bytes per parameter
- `float32/fp32`: 4 bytes per parameter  
- `bfloat16`: 2 bytes, better numerical stability
**Importance**: Halves memory usage (fp16 vs fp32) with minimal quality loss
**Practical**: Always use `--dtype=half` unless you have specific precision needs

## Memory Management

### GPU Memory Utilization
**What**: Percentage of GPU VRAM to use for the model
**Example**: `--gpu-memory-utilization=0.8` = use 80% of GPU memory
**Importance**: Prevents out-of-memory crashes, leaves room for OS and other processes
**Practical**: Start with 0.8, increase to 0.9+ once stable

### KV Cache
**What**: Stores previous tokens' key-value pairs for faster generation
**Size**: Grows with context length and batch size
**Importance**: Enables efficient text generation but consumes significant memory
**Practical**: Longer contexts = larger KV cache = less memory for batch processing

### Context Length (max_model_len)
**What**: Maximum number of tokens the model can process at once
**Example**: `--max-model-len=4096` = ~3000 words maximum
**Importance**: Longer contexts use exponentially more memory
**Practical**: Reduce if running out of memory; 2048-4096 is usually sufficient

### Block Size
**What**: Size of memory chunks allocated for KV cache
**Example**: `--block-size=16` = allocate memory in 16-token blocks
**Importance**: Smaller blocks = more efficient memory usage but higher overhead
**Practical**: Use 16 for balanced performance, 8 if memory-constrained

### Swap Space
**What**: Amount of CPU RAM to use for offloading GPU memory
**Example**: `--swap-space=4` = 4GB of CPU RAM as backup storage
**Importance**: Prevents crashes when GPU memory is full
**Practical**: Set to 4-8GB for safety

## Distributed Computing

### Tensor Parallelism (TP)
**What**: Split model layers across multiple GPUs
**Example**: `--tensor-parallel-size=2` = use 2 GPUs, each handles half the model
**Importance**: Enables running large models that don't fit on single GPU
**Practical**: Use minimum GPUs needed; more GPUs = communication overhead

### Ray
**What**: Distributed computing framework that vLLM uses for multi-GPU coordination
**Purpose**: Manages worker processes across GPUs, handles communication
**Importance**: Required for tensor parallelism but can cause deployment issues
**Practical**: Source of "getting stuck" issues; single GPU avoids Ray complexity

### Worker Processes
**What**: Individual processes running on each GPU in distributed setup
**Purpose**: Each worker handles part of the model computation
**Importance**: Must initialize successfully before serving starts
**Practical**: Failed workers cause deployment hangs

## Inference Engine Terms

### vLLM
**What**: High-performance inference engine optimized for large language models
**Features**: PagedAttention, continuous batching, tensor parallelism
**Importance**: Much faster than basic transformers library
**Practical**: Industry standard for production LLM serving

### Batching
**What**: Processing multiple requests simultaneously
**Types**: 
- Static batching: Fixed batch sizes
- Continuous batching: Dynamic request handling
**Importance**: Dramatically improves throughput
**Practical**: vLLM handles this automatically

### PagedAttention
**What**: vLLM's memory management technique for attention computation
**Purpose**: Reduces memory fragmentation, enables larger batch sizes
**Importance**: Key innovation that makes vLLM faster than alternatives
**Practical**: Works automatically, no configuration needed

## API and Serving

### OpenAI-Compatible API
**What**: API endpoints that match OpenAI's format
**Endpoints**: `/v1/completions`, `/v1/chat/completions`
**Importance**: Drop-in replacement for OpenAI API calls
**Practical**: Existing OpenAI code works without changes

### Tool Calling/Function Calling
**What**: Ability for model to invoke external functions/APIs
**Example**: `--tool-call-parser=hermes` enables structured tool invocations
**Importance**: Essential for agentic applications and RAG systems
**Practical**: Qwen models support tool calling with proper parser

### Streaming
**What**: Real-time token generation as model produces output
**Purpose**: Lower perceived latency, better user experience
**Importance**: Users see response immediately instead of waiting for completion
**Practical**: Add `"stream": true` to API requests

## Performance and Optimization

### Throughput
**What**: Number of tokens generated per second across all requests
**Measurement**: tokens/second or requests/second
**Importance**: Key metric for production systems
**Practical**: Higher with tensor parallelism and larger batch sizes

### Latency
**What**: Time from request to first token (TTFT) or complete response
**Types**:
- Time to First Token (TTFT): Initial response delay
- Inter-token latency: Time between generated tokens
**Importance**: User experience quality
**Practical**: Lower with single GPU, higher memory utilization

### Eager Execution
**What**: `--enforce-eager` disables graph optimizations
**Purpose**: More predictable execution, easier debugging
**Importance**: Use when troubleshooting memory or stability issues
**Practical**: Slower but more reliable; good for debugging

### Custom All-Reduce
**What**: Optimized communication for multi-GPU setups
**Purpose**: Faster data transfer between GPUs
**Importance**: Improves multi-GPU performance
**Practical**: Disable with `--disable-custom-all-reduce` if causing issues

## File Formats and Storage

### Safetensors
**What**: Secure tensor storage format, successor to pickle-based formats
**Advantages**: Faster loading, safer than `.bin` files
**Importance**: Prevents code injection, faster model loading
**Practical**: Preferred format for model weights

### Config.json
**What**: Model configuration file containing architecture details
**Contents**: Model type, dimensions, vocabulary size, etc.
**Importance**: Tells inference engine how to load the model
**Practical**: Check this file to understand model requirements

### Tokenizer Files
**What**: Files defining how text is converted to numbers
**Types**: `tokenizer.json`, `tokenizer_config.json`
**Importance**: Required for text processing
**Practical**: Must be present in model directory

## Troubleshooting Terms

### CUDA Out of Memory (OOM)
**What**: GPU runs out of video memory
**Causes**: Model too large, context too long, batch size too high
**Solutions**: Reduce memory utilization, shorter context, tensor parallelism
**Prevention**: Calculate memory requirements before deployment

### Process Hanging
**What**: Deployment gets stuck without error messages
**Common Causes**: Ray initialization, worker startup, model loading
**Solutions**: Use timeout, check logs, reduce complexity
**Prevention**: Test with single GPU first

### Invalid Argument Error
**What**: `torch.zeros CUDA error invalid argument`
**Cause**: Usually KV cache allocation with invalid tensor dimensions
**Solutions**: Reduce context length, change block size, update vLLM
**Context**: Often happens with newer models on older vLLM versions

## Quick Reference

### Memory Calculation
```
Model Memory = Parameters × Precision
Total Memory = Model Memory × 1.4 (includes KV cache + overhead)
```

### GPU Selection Rules
```
Single GPU: Total memory < GPU memory × 0.9
Multi-GPU: Use tensor parallelism when needed
```

### Common Parameter Patterns
```
Conservative: --gpu-memory-utilization=0.7 --max-model-len=2048
Balanced: --gpu-memory-utilization=0.85 --max-model-len=4096  
Aggressive: --gpu-memory-utilization=0.95 --max-model-len=8192
```

### Debugging Flags
```
--log-level=DEBUG --enforce-eager --disable-custom-all-reduce
```

Understanding these terms helps you:
1. **Plan deployments** based on hardware constraints
2. **Diagnose issues** using proper terminology  
3. **Optimize performance** by adjusting relevant parameters
4. **Communicate effectively** about deployment problems