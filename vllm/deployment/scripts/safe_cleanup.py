#!/usr/bin/env python3
"""
Safe cleanup for shared GPU server - only kills YOUR processes
Usage: python safe_cleanup.py
"""
import subprocess
import os
import getpass

def get_current_user():
    return getpass.getuser()

def safe_kill_user_processes():
    username = get_current_user()
    print(f"=== Cleaning processes for user: {username} ===")
    
    # Method 1: Python Ray shutdown
    try:
        import ray
        if ray.is_initialized():
            ray.shutdown()
            print("✓ Ray shutdown called")
        else:
            print("○ Ray not initialized")
    except:
        print("○ Ray not available or already down")
    
    # Method 2: Kill only YOUR processes
    try:
        # Find your ray processes
        result = subprocess.run(['pgrep', '-u', username, '-f', 'ray'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"Found {len(pids)} ray processes to kill")
            for pid in pids:
                try:
                    subprocess.run(['kill', pid], check=True)
                    print(f"✓ Killed ray process {pid}")
                except:
                    print(f"❌ Could not kill process {pid}")
        else:
            print("○ No ray processes found")
            
        # Find your vllm processes
        result = subprocess.run(['pgrep', '-u', username, '-f', 'vllm'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"Found {len(pids)} vllm processes to kill")
            for pid in pids:
                try:
                    subprocess.run(['kill', pid], check=True)
                    print(f"✓ Killed vllm process {pid}")
                except:
                    print(f"❌ Could not kill process {pid}")
        else:
            print("○ No vllm processes found")
            
    except Exception as e:
        print(f"❌ Error finding processes: {e}")

def cleanup_user_temp_files():
    username = get_current_user()
    print(f"\n=== Cleaning temp files for {username} ===")
    
    # Only clean user-specific temp files
    user_temp_dirs = [
        f'/tmp/ray/session_{username}*',
        f'/tmp/ray_{username}*',
        f'/dev/shm/ray_{username}*',
        os.path.expanduser('~/ray_results'),
        os.path.expanduser('~/.ray')
    ]
    
    for temp_pattern in user_temp_dirs:
        try:
            # Use shell expansion for patterns
            result = subprocess.run(f'rm -rf {temp_pattern}', 
                                  shell=True, capture_output=True)
            if result.returncode == 0:
                print(f"✓ Cleaned {temp_pattern}")
            else:
                print(f"○ {temp_pattern} not found or already clean")
        except Exception as e:
            print(f"❌ Could not clean {temp_pattern}: {e}")

def check_your_processes():
    username = get_current_user()
    print(f"\n=== Checking remaining processes for {username} ===")
    
    try:
        # Check your processes only
        result = subprocess.run(['ps', '-u', username, '-o', 'pid,cmd'], 
                              capture_output=True, text=True)
        lines = result.stdout.split('\n')
        ray_lines = [line for line in lines if 'ray' in line.lower()]
        vllm_lines = [line for line in lines if 'vllm' in line.lower()]
        
        if ray_lines:
            print("❌ Remaining ray processes:")
            for line in ray_lines:
                print(f"  {line}")
        else:
            print("✓ No ray processes running")
            
        if vllm_lines:
            print("❌ Remaining vllm processes:")
            for line in vllm_lines:
                print(f"  {line}")
        else:
            print("✓ No vllm processes running")
            
    except Exception as e:
        print(f"❌ Error checking processes: {e}")

if __name__ == "__main__":
    safe_kill_user_processes()
    cleanup_user_temp_files()
    check_your_processes()
    print("\n✅ Safe cleanup complete!")