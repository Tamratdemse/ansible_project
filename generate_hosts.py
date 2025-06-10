import os
from dotenv import load_dotenv
from jinja2 import Template

# Load .env file
load_dotenv()

# Read Jinja2 template
with open("inventory/hosts.ini.j2", "r") as f:
    template = Template(f.read())

# Render with .env values
rendered = template.render(
    webserver_ip=os.getenv("WEBSERVER_IP"),
    webserver_user=os.getenv("WEBSERVER_USER"),
    dbserver_ip=os.getenv("DBSERVER_IP"),
    dbserver_user=os.getenv("DBSERVER_USER"),
    python_path=os.getenv("PYTHON_PATH")
)

# Write the output to hosts.ini
with open("inventory/hosts.ini", "w") as f:
    f.write(rendered)

print("✅ Successfully generated inventory/hosts.ini from .env")
