#!/usr/bin/env python3
"""
vLLM Configuration-Based Deployment Script
Usage: python deploy_vllm.py --config <config_file.yaml> [--profile <profile_name>]

Examples:
  python deploy_vllm.py --config vllm_config.yaml --profile single_gpu
  python deploy_vllm.py --config vllm_config.yaml --profile debug
  python deploy_vllm.py --config vllm_config.yaml --profile multi_gpu
"""

import yaml
import argparse
import os
import subprocess
import sys

def load_config(config_file, profile):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            configs = yaml.safe_load(f)
        
        if profile not in configs:
            print(f"❌ Profile '{profile}' not found in config file")
            print(f"Available profiles: {list(configs.keys())}")
            return None
            
        config = configs[profile]
        print(f"✓ Loaded profile: {profile}")
        return config
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return None

def validate_config(config):
    """Validate required configuration fields"""
    required_sections = ['model', 'deployment', 'gpu', 'performance', 'features']
    
    for section in required_sections:
        if section not in config:
            print(f"❌ Missing required section: {section}")
            return False
    
    # Check model path exists
    model_path = config['model']['path']
    if not os.path.exists(model_path):
        print(f"❌ Model path does not exist: {model_path}")
        return False
    
    print("✓ Configuration validated")
    return True

def build_vllm_command(config):
    """Build vLLM serve command from configuration"""
    cmd = ["vllm", "serve", config['model']['path']]
    
    # Model settings
    cmd.extend([
        f"--dtype={config['model']['dtype']}",
    ])
    
    if config['model'].get('trust_remote_code', False):
        cmd.append("--trust-remote-code")
    
    # Deployment settings
    cmd.extend([
        f"--host={config['deployment']['host']}",
        f"--port={config['deployment']['port']}",
        f"--api-key={config['deployment']['api_key']}",
    ])
    
    # GPU settings
    cmd.extend([
        f"--tensor-parallel-size={config['gpu']['tensor_parallel_size']}",
        f"--gpu-memory-utilization={config['gpu']['gpu_memory_utilization']}",
    ])
    
    # Performance settings
    cmd.extend([
        f"--max-model-len={config['performance']['max_model_len']}",
        f"--block-size={config['performance']['block_size']}",
        f"--swap-space={config['performance']['swap_space']}",
    ])
    
    # Optional performance settings
    if 'cpu_offload_gb' in config['performance']:
        cmd.append(f"--cpu-offload-gb={config['performance']['cpu_offload_gb']}")
    
    # Feature settings
    if config['features'].get('tool_call_parser'):
        cmd.append(f"--tool-call-parser={config['features']['tool_call_parser']}")
    
    cmd.append(f"--log-level={config['features']['log_level']}")
    
    if config['features'].get('disable_custom_all_reduce', False):
        cmd.append("--disable-custom-all-reduce")
        
    if config['features'].get('enforce_eager', False):
        cmd.append("--enforce-eager")
    
    return cmd

def set_environment(config):
    """Set environment variables"""
    if 'visible_devices' in config['gpu']:
        os.environ['CUDA_VISIBLE_DEVICES'] = config['gpu']['visible_devices']
        print(f"✓ Set CUDA_VISIBLE_DEVICES={config['gpu']['visible_devices']}")

def print_deployment_info(config, cmd):
    """Print deployment information"""
    print("\n" + "="*60)
    print("🚀 vLLM DEPLOYMENT STARTING")
    print("="*60)
    print(f"Model: {config['model']['path']}")
    print(f"Host: {config['deployment']['host']}:{config['deployment']['port']}")
    print(f"GPUs: {config['gpu']['visible_devices']}")
    print(f"Tensor Parallel: {config['gpu']['tensor_parallel_size']}")
    print(f"Max Context: {config['performance']['max_model_len']}")
    print(f"Tool Parser: {config['features'].get('tool_call_parser', 'None')}")
    print("\nCommand:")
    print(" ".join(cmd))
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description='Deploy vLLM with YAML configuration')
    parser.add_argument('--config', required=True, help='Path to YAML config file')
    parser.add_argument('--profile', required=True, help='Configuration profile to use')
    parser.add_argument('--dry-run', action='store_true', help='Show command without executing')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config, args.profile)
    if not config:
        sys.exit(1)
    
    # Validate configuration
    if not validate_config(config):
        sys.exit(1)
    
    # Set environment
    set_environment(config)
    
    # Build command
    cmd = build_vllm_command(config)
    
    # Print info
    print_deployment_info(config, cmd)
    
    if args.dry_run:
        print("\n🔍 DRY RUN - Command would be executed:")
        print(" ".join(cmd))
        return
    
    # Execute command
    try:
        print("\n🚀 Starting vLLM server...")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Deployment stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Deployment failed with exit code {e.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()