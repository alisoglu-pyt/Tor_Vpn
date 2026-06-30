#!/usr/bin/env python3

"""Module version of start-vpn functionality so GUIs can import and call it."""

import subprocess
import sys
import os

# ========= CONFIG =========
TORRC_PATH = "/etc/tor/torrc"
TOR_USER = "debian-tor"   # Default user Tor runs as
TRANS_PORT = "9040"
DNS_PORT = "5353"
STATE_FILE = "/tmp/tor_tunnel_state"
# ==========================


def run(cmd, check=True):
    """Run a shell command."""
    print(f"[*] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def start_tor_tunnel():
    print("[*] Setting up Tor transparent proxy...")

    if subprocess.call("which tor", shell=True) != 0:
        print("[-] Tor is not installed. Please install Tor manually (e.g. 'apt install tor') and rerun this script.")
        raise RuntimeError("tor-not-installed")

    if not os.path.exists(f"{TORRC_PATH}.bak"):
        run(f"cp {TORRC_PATH} {TORRC_PATH}.bak")
        print(f"[*] Backup of torrc created at {TORRC_PATH}.bak")

    with open(TORRC_PATH, "r+") as f:
        content = f.read()
        if "TransPort" not in content:
            f.write(f"""

# Transparent proxy settings
VirtualAddrNetworkIPv4 10.192.0.0/10
AutomapHostsOnResolve 1
TransPort {TRANS_PORT}
DNSPort {DNS_PORT}
""")
            print("[*] torrc updated for transparent proxy.")

    run("systemctl restart tor")

    print("[*] Setting up iptables rules...")
    run("iptables -F")
    run("iptables -t nat -F")
    run(f"iptables -t nat -A OUTPUT -m owner --uid-owner {TOR_USER} -j RETURN")
    run("iptables -t nat -A OUTPUT -o lo -j RETURN")
    run(f"iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports {TRANS_PORT}")
    run(f"iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports {DNS_PORT}")

    print("[*] Tor tunnel is now active.")
    try:
        with open(STATE_FILE, "w") as f:
            f.write("on")
    except Exception as e:
        print(f"[!] Could not write state file {STATE_FILE}: {e}")


def is_socks_enabled():
    try:
        with open(TORRC_PATH, "r") as f:
            return "SocksPort" in f.read()
    except Exception:
        return False


def enable_socks():
    try:
        with open(TORRC_PATH, "r+") as f:
            content = f.read()
            if "SocksPort" not in content:
                f.write("\nSocksPort 9050\n")
                print("[*] Added SocksPort 9050 to torrc")
        run("systemctl restart tor")
        return True
    except Exception as e:
        print(f"[!] enable_socks error: {e}")
        return False


def disable_socks():
    try:
        with open(TORRC_PATH, "r") as f:
            lines = f.readlines()
        new_lines = [l for l in lines if not l.strip().startswith("SocksPort")]
        with open(TORRC_PATH, "w") as f:
            f.writelines(new_lines)
        run("systemctl restart tor")
        return True
    except Exception as e:
        print(f"[!] disable_socks error: {e}")
        return False


def get_exit_country():
    try:
        with open(TORRC_PATH, "r") as f:
            for line in f:
                if line.strip().startswith("ExitNodes"):
                    # Expect format: ExitNodes {us}
                    parts = line.split()
                    if len(parts) >= 2:
                        token = parts[1].strip()
                        if token.startswith("{") and token.endswith("}"):
                            return token.strip("{}")
        return None
    except Exception:
        return None


def set_exit_country(country_code: str):
    """Set ExitNodes to a country code (e.g. 'us') or 'any' to remove restriction."""
    try:
        # Read file and remove existing ExitNodes/StrictNodes lines
        with open(TORRC_PATH, "r") as f:
            lines = f.readlines()
        new_lines = [l for l in lines if not (l.strip().startswith("ExitNodes") or l.strip().startswith("StrictNodes"))]

        with open(TORRC_PATH, "w") as f:
            f.writelines(new_lines)
            if country_code and country_code.lower() != 'any':
                f.write(f"\nExitNodes {{{country_code}}}\nStrictNodes 1\n")
                print(f"[*] Set ExitNodes to {{{country_code}}}")
            else:
                print("[*] Removed ExitNodes/StrictNodes from torrc")

        run("systemctl restart tor")
        return True
    except Exception as e:
        print(f"[!] set_exit_country error: {e}")
        return False


def stop_tor_tunnel():
    print("[*] Stopping Tor transparent proxy...")

    print("[*] Flushing iptables rules...")
    run("iptables -F")
    run("iptables -t nat -F")

    if os.path.exists(f"{TORRC_PATH}.bak"):
        run(f"mv {TORRC_PATH}.bak {TORRC_PATH}")
        print("[*] torrc restored from backup.")

    run("systemctl restart tor")

    try:
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    except Exception as e:
        print(f"[!] Could not remove state file {STATE_FILE}: {e}")

    print("[*] Tor tunnel is now stopped.")


def main():
    if os.geteuid() != 0:
        print("[-] Please run this script as root (sudo).")
        sys.exit(1)

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} start|stop")
        sys.exit(1)

    if sys.argv[1] == "start":
        start_tor_tunnel()
    elif sys.argv[1] == "stop":
        stop_tor_tunnel()
    else:
        print(f"Usage: {sys.argv[0]} start|stop")
        sys.exit(1)


if __name__ == '__main__':
    main()
