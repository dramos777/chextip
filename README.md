# Chextip 2.0
## Description
This project automates the process of changing the IP address of an ATA (Analog Telephone Adapter) or controllers devices. The solution now includes a Bash script integrated with a Flask web interface and a MariaDB database to store and manage ATA configurations. The project no longer uses an inventory file, retrieving all necessary data directly from the database. The infrastructure is containerized using Docker Compose for easy deployment.

## Features
- Bash Script: Automates the ATA IP update process.
- Flask Web Interface: Manage ATAs via a web interface.
- MariaDB Integration: Stores device configurations and retrieves data dynamically.
- Docker Compose: Easily deploy the entire environment, including the web app and database.

## Web Interface Overview
The Flask web interface allows users to:

- View and manage devices configurations stored in the MariaDB database.
- Add or update devices records.
- Initiate the IP change process for a specific device via the web interface.

### Running the Web Interface with Docker Compose
Clone the Repository:

```
git clone https://github.com/dramos777/chextip.git
cd chextip
```
Start the Application: Ensure Docker and Docker Compose are installed, then run:
```
docker-compose up -d
```
Access the Web Interface: Open your browser and navigate to http://localhost:5000 to interact with the web interface.

## Docker Compose Setup
The project uses Docker Compose to run both the Flask application and the MariaDB database. The docker-compose.yaml defines the services and the required environment variables.

## Environment Variables
DB Variables:
```
MYSQL_DATABASE="condominios_db"
MYSQL_ROOT_PASSWORD="admin"
MYSQL_USER="admin"
MYSQL_PASSWORD="admin"
MYSQL_HOST="db"
```
SSH Variables:
```
SSH_USER="admin"
SSH_PORT="22"
SSH_PASSWORD="admin"
```
Telnet Variables:
```
TELNET_PORT="23"
TELNET_PASSWORD="admin"
REBOOT_COMMAND="reboot"
```
HTTP Variables:
```
HTTP_USER="admin"
HTTP_PASSWORD="admin"
HTTP_SS3530_PASS="admin"
HTTP_SS3532_PASS="admin"
HTTP_SS3540_PASS="admin"
HTTP_SS1530_PASS="admin"
HTTP_XPE3200_PASS="admin"
```
Network Prefix:
```
PREFIXIP="192.168."
```

## Bash Script Overview
The Bash script is integrated with the database to dynamically retrieve ATA configurations and update their IP addresses whether necessary. It interacts with the RouterOS system to modify DHCP leases and uses SSH, Telnet, and HTTP to communicate with devices.

## Usage
Run the script with the necessary arguments:

```
./chextip <phone_extension_number_or_device_id> [model]
```
The script retrieves the necessary data from the database, applies the IP changes, and logs the actions.

## Compatibility
This script works in GNU/Linux environments and supports the following ATA devices:

- Grandstream
    1. HT-503
    2. HT813
    3. HT814
    4. HT815
    5. GXW410X
- Linksys
    1. SPA 3000
    2. SPA 3102
- Intelbras
    1. ATA 200
    2. GKM2210T
    3. XPE3200
    4. SS3530
    5. SS3532
    6. SS3540
    7. SS1530
- Khomp
    1. 16-M4-L
- Nice
    1. Guarita MG3000

- Linear
    1. Guarita IP

## History
**v1.0 - 08/11/2023, Emanuel Dramos:**

- Initial script release.
- Added Selenium and automation.

**v2.0 - 21/10/2024, Emanuel Dramos:**

- Added Flask web interface.
- Integrated MariaDB for data management.
- Containerized application with Docker Compose.

**v2.3 - 21/10/2024, Emanuel Dramos:**

- Added compatibility with Intelbras: ss3530, ss3532, ss3540, ss1530, xpe3200; Nice: Guarita MG3000; Linear: Garita IP
- Added feature to update blocklist in pbx url
- Bug corrections
- Hidden buttons to non admin users

## Maintainer
Emanuel Dramos

- GitHub: dramos777
