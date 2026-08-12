# Home Lab Project: Custom Log Parsing and Splunk Ingestion Workflow

## 1. Lab Overview & Architecture
* **Environment:** Ubuntu Server virtual machine running in a local home lab environment.
* **Core Tools:** Splunk Enterprise, Python/Bash scripting for log processing, and Linux terminal utilities.
* **Objective:** Establish a hands-on IT and cybersecurity home lab to ingest, parse, and analyze structured security data. This project documents the complete workflow of generating custom JSON logs, resolving virtualization hurdles, managing Linux permissions, and configuring Splunk inputs.

## 2. Troubleshooting VM Clipboard Integration (Host-to-VM Copy/Paste)
* **The Challenge:** During the initial setup of the Ubuntu Server virtual machine, standard clipboard integration between the host operating system and the guest VM was disabled by default. This restricted the ability to copy commands, scripts, and configuration blocks directly from the host into the terminal.
* **The Fix:** 
  * Installed the appropriate virtualization guest integration packages within the Ubuntu Server terminal:
    ```bash
    sudo apt update && sudo apt install -y open-vm-tools open-vm-tools-desktop
    ```
  * Restarted the virtual machine services to enable seamless clipboard sharing, bi-directional drag-and-drop, and efficient command execution between the host workstation and the lab environment.

## 3. Data Parsing & Script Execution
* **Log Preparation:** Processed raw log data and structured it into a standardized JSON format.
* **Output Path:** Generated and saved the final structured log file to the user's home directory:
  ```text
  /home/admineddie/src/parsed_output.json
