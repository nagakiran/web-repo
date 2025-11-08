# Installing Python 3.13 on Ubuntu EC2 for Linkding

## Prerequisites - Install Build Dependencies

**IMPORTANT:** Linkding requires compiling packages like `uwsgi` and `psycopg`, so you need build tools installed first:

```bash
# Update package list
sudo apt update

# Install build essentials (gcc, make, etc.) and other dependencies
sudo apt install -y build-essential git curl libpq-dev libssl-dev

# Install software-properties-common for adding PPAs
sudo apt install -y software-properties-common
```

## Install Python 3.13

### Option 1: System-wide installation (recommended)

```bash
# Add deadsnakes PPA (provides newer Python versions)
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.13 with dev headers
sudo apt install -y python3.13 python3.13-venv python3.13-dev

# Verify installation
python3.13 --version
```

### Option 2: Let uv install Python 3.13

If you prefer not to install system-wide:

```bash
cd /opt/nagki/apps/git/linkding

# Let uv install Python 3.13
uv python install 3.13
```

## Run Linkding Setup

After installing all dependencies:

```bash
cd /opt/nagki/apps/git/linkding

# Pin the project to Python 3.13 (if using system Python)
uv python pin 3.13

# Now run your command - this will compile uwsgi and other packages
uv run manage.py createsuperuser --username=nagakiran --email=k.nagakiran@gmail.com
```

## Complete Installation Script (All-in-One)

Run this complete script on your EC2 instance:

```bash
# Install build dependencies
sudo apt update
sudo apt install -y build-essential git curl libpq-dev libssl-dev software-properties-common

# Install Python 3.13
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.13 python3.13-venv python3.13-dev

# Configure and run linkding
cd /opt/nagki/apps/git/linkding
uv python pin 3.13
uv run manage.py createsuperuser --username=nagakiran --email=k.nagakiran@gmail.com
```

## Why Python 3.13?

- Linkding requires Python `>=3.13`
- The `psycopg-binary==3.2.9` dependency has wheels for Python 3.13
- Python 3.14 is too new and doesn't have all required package wheels yet
- Python 3.12 is too old for linkding's requirements

## Troubleshooting

### Check which Python uv is using:

```bash
uv python list
uv python pin --show
```

### Common Errors and Solutions

**Error: `you need a C compiler to build uWSGI`**
- **Solution:** Install build-essential: `sudo apt install -y build-essential`

**Error: `psycopg-binary` doesn't have wheels for Python 3.14**
- **Solution:** Use Python 3.13 instead: `uv python pin 3.13`

**Error: `requires-python` value of `>=3.13`**
- **Solution:** You're using Python 3.12 or older, upgrade to 3.13

**Error: Failed to build `psycopg` or `psycopg-binary`**
- **Solution:** Install PostgreSQL development headers: `sudo apt install -y libpq-dev`

### Dependencies Explained

- **build-essential**: Provides gcc, g++, make, and other build tools
- **libpq-dev**: PostgreSQL client library headers (for psycopg)
- **libssl-dev**: SSL/TLS development files
- **python3.13-dev**: Python 3.13 header files and development tools
