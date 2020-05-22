from .base import *

DB_USER = "test"
DB_PASS = "testDBpass"
DB_DATABASE = "os3rl_dev"

# /dev/log doesn't exist everywhere
del LOGGING["handlers"]["syslog"]["address"]
