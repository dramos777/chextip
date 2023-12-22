# Change ATA IP Script

## Description
This Bash script is designed to automate the process of changing the IP address of an ATA (Analog Telephone Adapter) device. It reads from an inventory file informations about the infra enviroment and modifies the necessary configurations to update the ATA IP. The script utilizes various functions and environment variables to execute the necessary actions.

## Instructions
To use this script, follow the steps below:

1. Make sure you have the necessary environment variables properly configured.
2. Ensure that the required files and directories are in place.
4. Run the script with appropriate arguments.
5. Make sure RouterOS IP and phone extension is configured.
6. Make sure client-dhcp is configured in ATA
7. Make sure RouterOS leases is configured with ATA IP and properly comment.
8. Make sure you have the following dependencies installed:

- Python
- Selenium
- WebDriver (the script uses the Firefox browser)
- Telnet
- Sshpass

## Script Overview

- The script sets up necessary variables and checks for the presence of required utilities like `sshpass` and `telnet`.
- It imports functions from the main file and environment variables from the environment file.
- The script updates the environment variables and performs the necessary tasks to change the ATA IP address.
- It handles potential errors and logs the events in the designated log directory.

## Prerequisites
- Bash shell
- `sshpass` and `telnet` should be installed.
- Ensure the presence of the necessary configuration files and directories.
- Python
- Selenium

## Compatibility
The script is compatible with GNU/Linux environments. It has been tested on the following ATA devices:

- Grandstream (models: HT-503)
- Linksys (models: SPA 3000)
- Intelbras (models: ATA 200)
- Khomp (models: 16-M4-L)

## Usage
Run the script with the appropriate arguments, as demonstrated below:

```bash
./chextip <phone_extension_number> [model]
```

## History

v1.0 11/08/2023, Emanuel Dramos:
- Initial code
- README.md
- Push to github

v1.1 12/04/2023, Emanuel Dramos:
- Bug corrections

v1.2 12/22/2023
- Correction how chextip changes IP addres
- Correction how chextip remove connections
- IP range increased

### Maintainer
Emanuel Dramos
- **Github:** https://github.com/dramos777
