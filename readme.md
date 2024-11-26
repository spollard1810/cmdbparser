# CMDB Parser
A utility to match and parse CMDB data with hostname lists.

## Description
This script provides a GUI interface to:
1. Load a CMDB CSV file containing full device data
2. Load a simple hostname CSV file (single column of device names)
3. Generate a cleaned CSV with matched data for specific fields

## CSV File Requirements

### CMDB CSV (Input 1)
Must contain all these columns:
- name
- manufacturer
- model_id.name
- ip_address
- serial_number
- location
- firmware_version
- department
- operational_status

### Hostname CSV (Input 2)
A simple CSV file containing hostnames. Can be either:
- A single column (with or without header)
- Multiple columns (first column will be used as hostname)

### Output CSV
Generated file will be named `clean_csv_YYYY-MM-DD.csv` and will contain only:
- hostname (from CMDB 'name' field)
- ip_address
- model_id.name



