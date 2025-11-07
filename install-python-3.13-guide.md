# Installing Python 3.13 on Ubuntu EC2 for Linkding

## Quick Installation Steps

Run these commands on your EC2 instance:

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install -y software-properties-common

# Add deadsnakes PPA (provides newer Python versions)
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.13
sudo apt install -y python3.13 python3.13-venv python3.13-dev

# Verify installation
python3.13 --version
```

## Configure linkding to use Python 3.13

After installing Python 3.13:

```bash
cd /opt/nagki/apps/git/linkding

# Pin the project to Python 3.13
uv python pin 3.13

# Now run your command
uv run manage.py createsuperuser --username=nagakiran --email=k.nagakiran@gmail.com
```

## Alternative: Let uv install Python 3.13 for you

If the above doesn't work, `uv` can install Python 3.13 for you:

```bash
cd /opt/nagki/apps/git/linkding

# Install Python 3.13 via uv
uv python install 3.13

# Pin the project to use it
uv python pin 3.13

# Run your command
uv run manage.py createsuperuser --username=nagakiran --email=k.nagakiran@gmail.com
```

## Why Python 3.13?

- Linkding requires Python `>=3.13`
- The `psycopg-binary==3.2.9` dependency has wheels for Python 3.13
- Python 3.14 is too new and doesn't have all required package wheels yet
- Python 3.12 is too old for linkding's requirements

## Troubleshooting

If you still get errors, check which Python uv is using:

```bash
uv python list
uv python pin --show
```
