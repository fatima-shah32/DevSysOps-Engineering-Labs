# Lab 01 - Setting Up Jira and Python Environment

## Objective

Install Jira Software on Ubuntu, create a Python virtual environment, install Jira-related Python libraries, and verify Jira-Python connectivity.

## Tools Used

* Ubuntu Linux
* Java 11
* Jira Software 9.4.0
* Python 3
* Jira Python Library
* Requests
* Pandas
* Python Dotenv

## Project Structure

```text
DevSysOps-Engineering-Labs/
└── Jira-with-Python/
    └── Lab-01-Setting-Up-Jira-and-Python-Environment/
```

## Steps Performed

### 1. Updated System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Installed Dependencies

```bash
sudo apt install -y wget curl unzip python3-pip python3-venv openjdk-11-jdk
```

### 3. Installed Jira Software

```bash
wget https://product-downloads.atlassian.com/software/jira/downloads/atlassian-jira-software-9.4.0.tar.gz
tar -xzf atlassian-jira-software-9.4.0.tar.gz
```

### 4. Configured Jira

```bash
sudo mkdir -p /opt/jira-home
sudo mv atlassian-jira-software-9.4.0-standalone /opt/jira
```

### 5. Started Jira

```bash
cd /opt/jira/bin
./start-jira.sh
```

### 6. Created Python Virtual Environment

```bash
python3 -m venv jira-env
source jira-env/bin/activate
```

### 7. Installed Python Libraries

```bash
pip install jira requests python-dotenv pandas
```

### 8. Verified Installation

```bash
python test_installation.py
```

### 9. Tested Jira Connection

```bash
python jira_connection_test.py
```

## Outcome

* Jira Software installed successfully
* Python virtual environment configured
* Required libraries installed
* Jira connection verified using Python

## Conclusion

Successfully prepared a Jira and Python development environment for future Jira automation tasks.
