#!/usr/bin/env python3
# Created by willmet and indonesiancodeparty

import requests
import json
import time
import signal
import sys
from termcolor import colored

# Banner
def banner():
    print(colored("┌────────────────────────────────────────────┐", "cyan"))
    print(colored("│      Rate Limit Tester - POST Method       │", "cyan"))
    print(colored("│     Created by willmet x idcodeparty       │", "cyan"))
    print(colored("└────────────────────────────────────────────┘", "cyan"))
    print()

# Handle Ctrl+C
def signal_handler(sig, frame):
    print(colored("\n[!] Dihentikan oleh pengguna. Exit bersih.", "yellow"))
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Input
def get_inputs():
    url = input(colored("Masukkan URL target (contoh: https://target.com/api): ", "green"))
    payload_raw = input(colored("Masukkan payload JSON (contoh: {\"username\":\"admin\"}): ", "green"))
    total_req = input(colored("Berapa total request yang mau dikirim?: ", "green"))

    try:
        payload = json.loads(payload_raw)
    except json.JSONDecodeError:
        print(colored("[!] Payload tidak valid. Harus berupa JSON!", "red"))
        sys.exit(1)

    try:
        total = int(total_req)
    except ValueError:
        print(colored("[!] Jumlah request harus angka!", "red"))
        sys.exit(1)

    return url, payload, total

# Send requests with delay and counter
def send_requests(url, payload, total):
    for i in range(1, total + 1):
        try:
            response = requests.post(url, json=payload)
            status_code = response.status_code

            if status_code == 200:
                color = "green"
            elif status_code == 429:
                color = "red"
            elif status_code in [403, 401]:
                color = "yellow"
            else:
                color = "cyan"

            print(colored(f"[{i}/{total}] Status: {status_code} - {response.reason}", color))
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(colored(f"[!] Error saat request: {e}", "red"))
            time.sleep(1)

# Main
if __name__ == "__main__":
    banner()
    url, payload, total = get_inputs()
    print(colored("\n[+] Mulai mengirim POST request...\n", "blue"))
    send_requests(url, payload, total)
