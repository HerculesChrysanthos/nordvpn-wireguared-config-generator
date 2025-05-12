#!/usr/bin/env python3

import sys
import urllib.request
import json
import base64

# URLs
CREDENTIALS_URL = "https://api.nordvpn.com/v1/users/services/credentials"
RECOMMENDATIONS_URL = "https://api.nordvpn.com/v1/servers/recommendations?filters[servers_technologies][identifier]=wireguard_udp&limit=1"
ALL_SERVERS_URL = "https://api.nordvpn.com/v1/servers"

# Paths
CONFIG_TEMPLATE_PATH = "wireguard_config.template"
OUTPUT_CONFIG_PATH = "wg0.conf"

# Token input
if len(sys.argv) < 2:
    print("Usage: python3 nordvpn_wg_config.py <api_token> [server_hostname]")
    sys.exit(1)

api_token = sys.argv[1]
server_hostname = sys.argv[2] if len(sys.argv) > 2 else None

# Auth header
encoded_token = base64.b64encode(f"token:{api_token}".encode()).decode()
auth_headers = {"Authorization": f"Basic {encoded_token}"}

def terminate(msg):
    print(f"❌ {msg}")
    sys.exit(1)

def fetch_data(url, headers=None):
    request = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        terminate(f"Failed to fetch data: {e.reason}")

# Step 1: Get credentials (private key)
credentials = fetch_data(CREDENTIALS_URL, auth_headers)
private_key = credentials.get("nordlynx_private_key")
if not private_key:
    terminate("Could not retrieve WireGuard private key. Invalid token?")

# Step 2: Get server info
if server_hostname:
    servers = fetch_data(ALL_SERVERS_URL)
    print(servers)
    matching_servers = [s for s in servers if s["hostname"] == server_hostname]
    if not matching_servers:
        terminate(f"Server not found: {server_hostname}")
    server = matching_servers[0]
else:
    recommendations = fetch_data(RECOMMENDATIONS_URL)
    if not recommendations:
        terminate("No recommended servers found.")
    server = recommendations[0]

server_name = server["name"]
server_ip = server["station"]
technologies = server.get("technologies", [])

wg_tech = next((t for t in technologies if t["identifier"] == "wireguard_udp"), None)
if not wg_tech:
    terminate("WireGuard UDP not supported on selected server.")

public_key = next((m["value"] for m in wg_tech["metadata"] if m["name"] == "public_key"), None)
if not public_key:
    terminate("Public key not found for selected server.")

# Step 3: Generate config from template
try:
    with open(CONFIG_TEMPLATE_PATH, "r") as f:
        template = f.read()
except FileNotFoundError:
    terminate(f"Missing config template file: {CONFIG_TEMPLATE_PATH}")

config = template.format(
    private_key=private_key,
    public_key=public_key,
    server_ip=server_ip
)

with open(OUTPUT_CONFIG_PATH, "w") as f:
    f.write(config)

print(f"✅ WireGuard config created as {OUTPUT_CONFIG_PATH} for server: {server_name}")
