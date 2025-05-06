import os

import orjson
from pythonping import ping

HOSTS_FILE = os.path.join(os.path.dirname(__file__), "hosts.json")


def load_hosts():
    try:
        with open(HOSTS_FILE, "rb") as f:
            return orjson.loads(f.read())
    except FileNotFoundError:
        print(f"Error: File not found at '{HOSTS_FILE}'")
        return None
    except orjson.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in '{HOSTS_FILE}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_hosts(hosts):
    with open(HOSTS_FILE, "wb") as f:
        f.write(orjson.dumps(hosts))


def check_servers(CHECK_INTERVAL):
    servers = load_hosts()
    for server in servers:
        try:
            response = ping(server["ip"], count=1, timeout=1)
        except Exception:
            server["alive"] = False
        if response.success() == server["alive"]:
            server["duration"] += CHECK_INTERVAL
        else:
            if server["attempt"] > 2:
                server["duration"] = 0
                server["attempt"] = 0
                server["alive"] = response.success()
            else:
                server["attempt"] += 1
    save_hosts(servers)
