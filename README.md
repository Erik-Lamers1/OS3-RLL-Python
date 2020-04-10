# OS3 Rocket League Ladder
[![Build Status](https://travis-ci.org/Erik-Lamers1/OS3-RLL-Python.svg?branch=master)](https://travis-ci.org/Erik-Lamers1/OS3-RLL-Python)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repo is a Python(3) implementation of the original [OS3 Rocket League Ladder](https://github.com/Erik-Lamers1/OS3-Rocket-League-Ladder) written in PHP.

This implementation makes heavy use of the [Python discord bot](https://discordpy.readthedocs.io/en/latest/).  
The idea is that players participating in the ladder can control the challenges and result entirely from discord.

## Running the bot
### Creating the database
```shell script
cd OS3-RLL-Python
mysql -e "CREATE DATABASE IF NOT EXISTS os3rl"
cat deployment/database_schema.sql | mysql
```

### Running on CLI
```shell script
cd 
python setup.py install
export DISCORD_TOKEN=<token>
export DB_USER=<database_username>
export DB_PASS=<database_password>
os3-rocket-league-ladder
```

### Running as a service
```shell script
# Create the env and service files
cat <<EOF > /etc/default/os3-rocket-league-ladder
DISCORD_TOKEN=<token>
DB_USER=<database_username>
DB_PASS=<database_password>
EOF

cat <<EOF > /etc/systemd/system/os3-rocket-league-ladder.service
[Unit]
Description=Rocket League Ladder Python
After=network-online.target
StartLimitIntervalSec=0

[Service]
EnvironmentFile=/etc/default/os3-rocket-league-ladder
Type=simple
Restart=always
RestartSec=5
User=rrl
ExecStart=/usr/local/bin/os3-rocket-league-ladder

[Install]
WantedBy=multi-user.target
EOF

# Add the user
useradd --system --shell /bin/false rrl

# Enable and start the service
systemctl daemon-reload
systemctl enable os3-rocket-league-ladder.service
systemctl start os3-rocket-league-ladder.service
```

## Setting up a development environment
If you want work on the OS3-RLL-Python bot, great!  
Here is how to setup your env
```shell script
git clone git@github.com:Erik-Lamers1/OS3-RLL-Python.git
cd OS3-RLL-Python
apt-get install virtualenvwrapper tox
mkvirtualenv -p $(which python3.6) -a $(pwd) OS3-RLL-Python
pip install -r requirements/development.txt
pre-commit install
# And you are good to go
```

## Running the tests
Either run `tox` or run `pytest` from within your venv.