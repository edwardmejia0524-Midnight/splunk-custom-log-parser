import re
import json
from collections import defaultdict

def parse_auth_log(file_path):
    pattern = re.compile(
        r'(?P<month>[A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+)\s+'
        r'(?P<host>\S+)\s+'
        r'sshd\[\d+\]:\s+'
        r'(?P<status>Accepted|Failed)\s+.*?\s+'
        r'(?:for\s+(?:invalid\s+user\s+)?(?P<user>\S+)\s+)?'
        r'from\s+(?P<ip>\d+\.\d+\.\d+\.\d+)'
    )
    failed_attempts = defaultdict(int)
    parsed_logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = pattern.search(line)
                if match:
                    data = match.groupdict()
                    parsed_logs.append(data)
                    if data['status'] == 'Failed':
                        failed_attempts[data['ip']] += 1
        return parsed_logs, failed_attempts
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return [], {}

def export_to_json(logs, failures, output_path="src/parsed_output.json"):
    output_data = {
        "total_entries": len(logs),
        "failed_summary": dict(failures),
        "logs": logs
    }
    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"Report successfully exported to {output_path}")

if __name__ == "__main__":
    logs, failures = parse_auth_log("sample_logs/auth.log")
    print(f"Successfully parsed {len(logs)} log entries.")
    print("\nFailed Login Summary by IP:")
    for ip, count in failures.items():
        print(f"  - IP {ip}: {count} failed attempt(s)")
    
    export_to_json(logs, failures)
