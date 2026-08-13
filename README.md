# Home Lab Project: Custom Log Parsing, Version Control, and Splunk Ingestion Workflow

## Repository Structure

```text
splunk-custom-log-parser/
├── README.md
├── scripts/
│   └── log_parser.py           # Python script for generating/parsing logs
├── configs/
│   ├── inputs.conf             # Splunk input monitor and TCP receiver configuration
│   └── indexes.conf            # Custom index definition (security_lab_index)
├── data/
│   └── parsed_output.json      # Structured JSON log output
└── .gitignore
```

---

## 1. Lab Overview & Architecture

* **Environment:** Ubuntu Server virtual machine running in a local VMware-based home lab environment.
* **Core Tools:** Splunk Enterprise, Splunk Universal Forwarder, Python scripting for log processing, Linux terminal utilities, Git, and GitHub.
* **Objective:** Establish a comprehensive hands-on IT and cybersecurity home lab to generate, parse, ingest, version control, and analyze structured security data. This project documents the complete end-to-end workflow from hypervisor clipboard troubleshooting to secure GitHub remote publishing and Splunk log monitoring.

---

## 2. Troubleshooting VM Clipboard Integration (Host-to-VM Copy/Paste)

### The Challenge
During the initial deployment of the Ubuntu Server virtual machine, standard clipboard integration between the host operating system and the guest VM was disabled by default. This restricted the ability to copy configuration blocks, scripts, and administrative commands directly from the host into the terminal.

### The Fix & Diagnostic Commands
1. Checked active system services and updated package lists:
```bash
sudo apt update
sudo systemctl status
```

2. Installed the appropriate virtualization guest integration packages within the Ubuntu Server terminal to restore bi-directional copy/paste and drag-and-drop capabilities:
```bash
sudo apt update && sudo apt install -y open-vm-tools open-vm-tools-desktop
```

3. Restarted the virtual machine services and verified active guest daemon status:
```bash
sudo systemctl restart open-vm-tools
sudo systemctl enable open-vm-tools
```

---

## 3. Data Parsing & Script Execution

### Log Preparation
Processed raw log data and structured it into a standardized JSON format to ensure compatibility with Splunk's event parser. By converting raw strings into JSON *before* ingestion, we significantly reduce the processing overhead on the Splunk indexer.

* Output Path: Generated and saved the final structured log file directly to the working directory: `/home/admineddie/src/parsed_output.json`

### Implementation Script (Python Example)
Below is the full implementation script demonstrating how raw log lines are parsed, converted, and written into a structured JSON format:

```python
import json
from datetime import datetime

def parse_log_line(raw_line):
    # Custom parsing logic for security events
    parts = raw_line.strip().split(" - ")
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_level": parts[0],
        "source_ip": parts[1],
        "action": parts[2],
        "status": "SUCCESS"
    }
    return log_entry

# Sample execution and file write operations
if __name__ == "__main__":
    raw_sample = "INFO - 192.168.1.50 - Authentication Attempt"
    parsed_data = parse_log_line(raw_sample)
    
    output_filepath = "/home/admineddie/src/parsed_output.json"
    with open(output_filepath, "w") as f:
        json.dump(parsed_data, f, indent=4)
    print(f"Successfully wrote parsed log to {output_filepath}")
```

---

## 4. Linux File Permissions & Directory Management

To ensure Splunk Enterprise (running under its dedicated service account) has proper read access to the generated logs without triggering permission errors or blocked ingestion streams, file access control lists and ownership were configured using the following terminal commands:

```bash
mkdir -p /home/admineddie/src/
sudo chown -R admineddie:splunk /home/admineddie/src/
sudo chmod 750 /home/admineddie/src/parsed_output.json
ls -la /home/admineddie/src/
```

---

## 5. Splunk Configuration & Data Ingestion Pipeline

### Data Receiver & Universal Forwarder Configuration
1. **Receiver Setup (Port 9997):** Configured Splunk Enterprise to listen on TCP port `9997` under `[splunktcp://9997]` in `inputs.conf` to receive forwarded data streams.
2. **Management Port Resolution (Port 8090):** Resolved a management port conflict with Splunk Enterprise (which binds to default port `8089`) by reconfiguring the Splunk Universal Forwarder daemon to utilize port `8090`.
3. **Forwarding Rule:** Established active log forwarding from the Universal Forwarder (`127.0.0.1:9997`) to push local data streams into the Splunk Enterprise indexer.

### Data Input Setup & Parsing
1. Configured file monitoring for the absolute log path: `/home/admineddie/src/parsed_output.json`.
2. Assigned **Sourcetype** to `_json`. Splunk natively parses key-value pairs and arrays (`timestamp`, `total_entries`, `logs{}.ip`, `logs{}.user`, `logs{}.status`) during indexing without requiring custom Regex extraction rules in `props.conf` or `transforms.conf`.
3. Routed event streams directly to the designated custom index: `security_lab_index`.

---

## 6. Splunk Search & Analysis Validation

To verify the ingestion pipeline and test the newly extracted structured JSON fields, the following Splunk Processing Language (SPL) queries were executed in the Search & Reporting app:

```spl
# 1. Verify general ingestion and field extraction
index="security_lab_index" sourcetype="_json"

# 2. Table formatted array fields extracted from JSON payload
index=security_lab_index | table _time host total_entries logs{}.user logs{}.ip logs{}.status

# 3. Create a statistical timechart of events grouped by action
index="security_lab_index" sourcetype="_json" | timechart count by action
```

---

## 7. Repository Structure & Version Control Setup Steps

### Repository Initialization and Remote Push Steps Performed
1. Created project directory layout:
   ```bash
   mkdir -p ~/splunk-custom-log-parser/{scripts,configs,data}
   cd ~/splunk-custom-log-parser
   git init
   ```

2. Staged and committed initial project files to local version control:
   ```bash
   git add .
   git commit -m "Initial commit of custom log parser lab workflow and configs"
   ```

3. Configured remote repository tracking and pushed to the `main` branch:
   ```bash
   git remote add origin [https://github.com/edwardmejia0524-Midnight/splunk-custom-log-parser.git](https://github.com/edwardmejia0524-Midnight/splunk-custom-log-parser.git)
   git branch -M main
   git push -u origin main
   ```

### File & Directory Descriptions
* `README.md` – Complete technical project documentation, architectural overview, and troubleshooting steps.
* `scripts/` – Contains Python log generation and JSON formatting logic.
* `configs/` – Contains Splunk `inputs.conf` and `indexes.conf` ingestion definitions.
* `data/` – Contains sample raw input logs and parsed output JSON files.
