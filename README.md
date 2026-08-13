# Home Lab Project: Custom Log Parsing, Version Control, and Splunk Ingestion Workflow

## 1. Lab Overview & Architecture

* Environment: Ubuntu Server virtual machine running in a local VMware-based home lab environment.
* Core Tools: Splunk Enterprise, Python scripting for log processing, Linux terminal utilities, Git, and GitHub.
* Objective: Establish a comprehensive hands-on IT and cybersecurity home lab to generate, parse, ingest, version control, and analyze structured security data. This project documents the complete end-to-end workflow from hypervisor clipboard troubleshooting to secure GitHub remote publishing and Splunk log monitoring.

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

## 4. Linux File Permissions & Directory Management

To ensure Splunk Enterprise (running under its dedicated service account) has proper read access to the generated logs without triggering permission errors or blocked ingestion streams, file access control lists and ownership were configured using the following terminal commands:

```bash
mkdir -p /home/admineddie/src/
sudo chown -R admineddie:splunk /home/admineddie/src/
sudo chmod 750 /home/admineddie/src/parsed_output.json
ls -la /home/admineddie/src/
```

## 5. Splunk Configuration & Data Ingestion Workflow

Once the JSON logs were generated and permissions were secured, the next phase was actively configuring Splunk to monitor and ingest the data. 

### Data Input Setup
1. Navigated to **Settings > Data > Data Inputs** within the Splunk Web UI.
2. Selected **Files & Directories** and clicked **New Local File & Directory**.
3. Provided the absolute path to the generated log: `/home/admineddie/src/parsed_output.json`.
4. Set the **Sourcetype** to `_json`. Because the Python script already structured the data into JSON, Splunk natively parses the key-value pairs (`timestamp`, `event_level`, `source_ip`, `action`, `status`) during the indexing phase without requiring complex Regex extraction rules in `props.conf` or `transforms.conf`.
5. Assigned the input to a dedicated custom index (e.g., `security_lab_index`) to maintain strict data segregation from internal Splunk diagnostic logs.

## 6. Splunk Search & Analysis Validation

To verify the ingestion pipeline and test the newly extracted fields, the following Splunk Processing Language (SPL) queries were executed in the Search & Reporting app:

```spl
# 1. Verify data is arriving and fields are properly extracted
index="security_lab_index" sourcetype="_json"

# 2. Create a statistical timechart of events grouped by the extracted 'action' field
index="security_lab_index" sourcetype="_json" | timechart count by action

# 3. Identify and count the frequency of actions tied to specific IP addresses
index="security_lab_index" sourcetype="_json" | stats count by source_ip, status
```

## 7. Repository Structure & Version Control Setup Steps

* Repository Initialization and Remote Push Steps Performed:
  1. Created a new local working directory and initialized a local git repository:
     `mkdir -p ~/src && cd ~/src && git init`

  2. Created the documentation and source script files locally:
     `touch README.md parsed_output.json`

  3. Staged and committed the initial project files to local version control:
     `git add .`
     `git commit -m "Initial commit of custom log parser lab workflow and script"`

  4. Generated a GitHub Personal Access Token (PAT) with repository Contents (Read and write) permissions via GitHub Account Settings -> Developer Settings -> Personal access tokens.

  5. Configured remote repository tracking and pushed code using the secure token:
     `git remote add origin https://github.com/edwardmejia0524-Midnight/splunk-custom-log-parser.git`
     `git push -u origin main`
     *(Entered GitHub username: `edwardmejia0524-Midnight` and pasted the generated PAT as the password prompt).*

* File Descriptions:
  * `README.md` - Technical project documentation and workflow breakdown.
  * `parsed_output.json` - Sample structured output log file.
