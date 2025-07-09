# instabot_manager.py

from instagrapi import Client
import json
import threading

accounts = {}

def load_accounts(file='accounts.json'):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[!] File {file} not found. Returning empty accounts.")
        return {}
    except json.JSONDecodeError:
        print(f"[!] Error decoding JSON from {file}. Returning empty accounts.")
        return {}

def save_accounts(accounts, file='accounts.json'):
    with open(file, 'w') as f:
        json.dump(accounts, f, indent=2)

def login_account(username, password, proxy=None):
    cl = Client()
    if proxy:
        cl.set_proxy(proxy)
    cl.login(username, password)
    return cl

def report_user(client, target_username):
    user_id = client.user_id_from_username(target_username)
    result = client.report_user(user_id, reason="it's pretending to be someone else")
    print(f"[+] Report sent from {client.username} -> {target_username} = {result}")

def perform_bulk_report(target_username):
    for acc, config in accounts.items():
        def task():
            try:
                print(f"[*] Logging in with {acc}")
                cl = login_account(config['username'], config['password'], config.get('proxy'))
                report_user(cl, target_username)
            except Exception as e:
                print(f"[!] Failed for {acc}: {e}")
        threading.Thread(target=task).start()

if __name__ == "__main__":
    accounts = load_accounts()
    target = input("Enter username to report: ")
    perform_bulk_report(target)
