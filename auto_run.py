import time
import subprocess

# Run every 60 seconds
INTERVAL = 60 

print(f"Starting auto-runner. Press Ctrl+C to stop.")

try:
    while True:
        print(f"\n--- Running Pipeline at {time.strftime('%X')} ---")
        # This tells Python to run your main.py file exactly as if you typed it in the terminal
        subprocess.run(["python", "main.py"])
        print(f"Sleeping for {INTERVAL} seconds...")
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\nAuto-runner stopped manually.")