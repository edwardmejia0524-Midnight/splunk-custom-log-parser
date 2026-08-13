import json
import random
import time
from datetime import datetime

# Define sample data fields for security event simulation
event_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
actions = ["LOGIN", "LOGOUT", "FILE_ACCESS", "CONFIG_CHANGE", "API_REQUEST"]
statuses = ["SUCCESS", "FAILED", "UNAUTHORIZED"]

def generate_security_event():
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_level": random.choice(event_levels),
        "source_ip": f"192.168.1.{random.randint(1, 254)}",
        "user": f"user_{random.randint(100, 110)}",
        "action": random.choice(actions),
        "status": random.choice(statuses),
        "details": "Simulated security event log for home lab analysis."
    }
    return event

def main():
    output_file = "/var/log/custom_app/app.log"
    print(f"Generating logs and writing to {output_file}...")
    
    # Writing a few sample JSON events to the file
    events = [generate_security_event() for _ in range(10)]
    
    with open(output_file, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")
            
    print("Log generation complete.")

if __name__ == "__main__":
    main()
