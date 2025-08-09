# =============================================================================
# 3. check_gpu_usage.py - Check GPU usage on shared server
# =============================================================================
"""
Check GPU usage on shared server
Usage: python check_gpu_usage.py
"""
import subprocess
import getpass

def check_gpu_usage():
    username = getpass.getuser()
    print(f"=== GPU Usage on Shared Server (Current user: {username}) ===")
    
    try:
        # Get detailed GPU info
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        print(result.stdout)
        
        # Parse for process info
        print("\n=== Active GPU Processes ===")
        lines = result.stdout.split('\n')
        process_section = False
        found_processes = False
        
        for line in lines:
            if 'Processes:' in line:
                process_section = True
                continue
            elif process_section and '|' in line and 'PID' not in line and line.strip():
                if 'No running processes found' not in line:
                    # Extract process info
                    parts = line.split('|')
                    if len(parts) >= 5:
                        gpu_info = parts[1].strip()
                        pid_info = parts[2].strip()
                        process_name = parts[4].strip() if len(parts) > 4 else "Unknown"
                        memory_info = parts[5].strip() if len(parts) > 5 else "Unknown"
                        
                        # Check if it's your process
                        try:
                            pid = pid_info.split()[0]
                            user_check = subprocess.run(['ps', '-p', pid, '-o', 'user='], 
                                                      capture_output=True, text=True)
                            process_user = user_check.stdout.strip()
                            
                            ownership = "👤 YOURS" if process_user == username else f"👥 {process_user}"
                            print(f"GPU {gpu_info}: PID {pid} ({ownership}) - {process_name} - {memory_info}")
                            found_processes = True
                        except:
                            print(f"GPU {gpu_info}: {pid_info} - {process_name} - {memory_info}")
                            found_processes = True
        
        if not found_processes:
            print("✓ No active GPU processes found")
            
    except Exception as e:
        print(f"❌ Error checking GPU usage: {e}")

    # Check available GPUs for your use
    print(f"\n=== Available GPUs for {username} ===")
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True)
        
        lines = result.stdout.strip().split('\n')
        for line in lines:
            parts = line.split(', ')
            if len(parts) >= 4:
                gpu_id, mem_used, mem_total, utilization = parts
                mem_used_gb = int(mem_used) / 1024
                mem_total_gb = int(mem_total) / 1024
                mem_free_gb = mem_total_gb - mem_used_gb
                
                if int(utilization) < 10 and mem_free_gb > 8:
                    status = "✅ Available"
                elif int(utilization) < 50 and mem_free_gb > 4:
                    status = "⚠️ Partially available"
                else:
                    status = "❌ Busy"
                
                print(f"GPU {gpu_id}: {mem_free_gb:.1f}GB free, {utilization}% util - {status}")
                
    except Exception as e:
        print(f"❌ Error checking GPU availability: {e}")

if __name__ == "__main__":
    check_gpu_usage()