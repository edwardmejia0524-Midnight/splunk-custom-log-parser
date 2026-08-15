import os
import json
from collections import Counter

LOG_PATH = "sample_logs/auth.log"
OUTPUT_PATH = "data/parsed_output.json"

def parse_logs():
    if not os.path.exists(LOG_PATH):
        print(f"Error: The file {LOG_PATH} was not found.")
        return [], []

    failed_ips = []
    parsed_entries = []

    with open(LOG_PATH, "r") as f:
        for line in f:
            if "Failed password" in line:
                parts = line.strip().split()
                ip = "Unknown"
                for i, part in enumerate(parts):
                    if part == "from":
                        ip = parts[i+1]
                        break
                failed_ips.append(ip)
                parsed_entries.append({
                    "timestamp": " ".join(parts[:3]), 
                    "event": "Failed Login", 
                    "source_ip": ip
                })

    print(f"Successfully parsed {len(parsed_entries)} log entries.")
    return failed_ips, parsed_entries

def export_to_json(entries, output_path=OUTPUT_PATH):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(entries, f, indent=4)
    print(f"Exported parsed logs to {output_path}")

if __name__ == "__main__":
    failures, entries = parse_logs()
    if failures:
        print("\nFailed Login Summary by IP:")
        for ip, count in Counter(failures).items():
            print(f"  - IP {ip}: {count} failed attempt(s)")
    if entries:
        export_to_json(entries)
