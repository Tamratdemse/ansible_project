import os
from dotenv import load_dotenv
from jinja2 import Template

# Load .env file (ensure FRONTEND_IP and FRONTEND_USER are defined here)
load_dotenv()

# Read Jinja2 template
# Ensure inventory/hosts.ini.j2 uses {{ frontend_ip }} and {{ frontend_user }}
with open("inventory/hosts.ini.j2", "r") as f:
    template = Template(f.read())

# Render with .env values
rendered = template.render(
    webserver_ip=os.getenv("WEBSERVER_IP"),
    webserver_user=os.getenv("WEBSERVER_USER"),
    dbserver_ip=os.getenv("DBSERVER_IP"),
    dbserver_user=os.getenv("DBSERVER_USER"),
    frontend_ip=os.getenv("FRONTEND_IP"),   # Renamed from staticweb_ip
    frontend_user=os.getenv("FRONTEND_USER"), # Renamed from staticweb_user
    python_path=os.getenv("PYTHON_PATH")
)

# Write the output to hosts.ini
with open("inventory/hosts.ini", "w") as f:
    f.write(rendered)

print("✅ Successfully generated inventory/hosts.ini from .env")
