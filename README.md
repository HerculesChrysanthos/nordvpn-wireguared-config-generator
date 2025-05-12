📡 NordVPN WireGuard Config Generator

This tool allows you to generate a fully working WireGuard .conf file using your NordVPN API access token. You can either select a specific server (like gr67.nordvpn.com) or let the script choose the best recommended one for you.

✅ Features

- Supports custom server selection (e.g., us1234.nordvpn.com)
- Automatically fetches your WireGuard private key using your NordVPN token
- Builds a valid wg0.conf using server info and public key
- Fully compatible with macOS, Linux, and WireGuard clients

📦 Files Included

| File Name                   | Description                                          |
|-----------------------------| ---------------------------------------------------- |
| `run.sh`                    | Bash script to run the config generator              |
| `generate_config.py`        | Python script that fetches credentials + server info |
| `wireguard_config.template` | Template used to create final WireGuard config       |
| `wg0.conf`                  | Final output configuration (created after run)       |

🚀 Usage Instructions
1. Clone or download the project

git clone https://github.com/HerculesChrysanthos/nordvpn-wireguared-config-generator
cd nordvpn-wireguared-config-generator

2. Run bash file


`./run.sh`