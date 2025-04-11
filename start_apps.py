#!/usr/bin/env python3
import subprocess
import os
import sys
import time
import signal
import atexit

def kill_processes(processes):
    """Kill all running processes when the script exits."""
    for process in processes:
        if process.poll() is None:  # If process is still running
            try:
                process.terminate()
                print(f"Terminated process {process.pid}")
            except:
                pass
        
        # Close log files if they exist
        if hasattr(process, 'stdout_log'):
            process.stdout_log.close()
        if hasattr(process, 'stderr_log'):
            process.stderr_log.close()

def main():
    # Store the processes to be able to terminate them later
    processes = []
    
    # Register the cleanup function to run on exit
    atexit.register(kill_processes, processes)
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nCaught Ctrl+C. Shutting down all applications...")
        kill_processes(processes)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Define the applications to start
    apps = [
        {"name": "Main App", "script": "app.py", "port": 8501},
        {"name": "Data Analysis", "script": "analysis.py", "port": 8502},
        {"name": "Admin Interface", "script": "admin.py", "port": 8503}
    ]
    
    # Start each application
    for app in apps:
        print(f"Starting {app['name']} on port {app['port']}...")
        
        # Build the command
        cmd = [
            "python3", "-m", "streamlit", "run", 
            app["script"], 
            "--server.port", str(app["port"]),
            "--server.headless", "true"
        ]
        
        # Create log files for stdout and stderr
        stdout_log = open(f"{app['script']}.stdout.log", "w")
        stderr_log = open(f"{app['script']}.stderr.log", "w")
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=stdout_log,
            stderr=stderr_log,
            text=True
        )
        
        # Store log file handles to close them later
        process.stdout_log = stdout_log
        process.stderr_log = stderr_log
        
        processes.append(process)
        
        # Wait a moment to ensure the process starts
        time.sleep(1)
        
        # Check if the process is still running
        if process.poll() is None:
            print(f"✅ {app['name']} started successfully at http://localhost:{app['port']}")
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start {app['name']}:")
            print(f"Error: {stderr}")
            # Kill any processes that were started successfully
            kill_processes(processes)
            sys.exit(1)
    
    print("\n🚀 All applications started successfully!")
    print("\nAccess your applications at:")
    print("  • Main App: http://localhost:8501")
    print("  • Data Analysis: http://localhost:8502")
    print("  • Admin Interface: http://localhost:8503")
    print("\nPress Ctrl+C to shut down all applications.\n")
    
    # Keep the script running to maintain the processes
    try:
        while True:
            # Check if any process has terminated unexpectedly
            for i, process in enumerate(processes):
                if process.poll() is not None:
                    stdout, stderr = process.communicate()
                    app = apps[i]
                    print(f"⚠️ {app['name']} terminated unexpectedly.")
                    if stderr:
                        print(f"Error: {stderr}")
            
            # Sleep to avoid high CPU usage
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all applications...")
        kill_processes(processes)

if __name__ == "__main__":
    main()
