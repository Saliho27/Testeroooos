from instabot import Bot
import time
import os

# To store accounts and proxies
# Each account will be a dictionary containing 'username', 'password', 'proxy'
accounts_data = []
proxies_data = [] # Can be used later to assign a proxy from an existing list

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def login_and_control(account_info):
    bot = Bot()
    try:
        # If a proxy is specified for the account, use it
        if account_info["proxy"]:
            bot.proxy(account_info["proxy"])
        else:
            # If no proxy, instabot will use the local IP automatically
            print(f"Account: {account_info['username']} will use a direct connection (local IP).")

        if bot.login(username=account_info["username"], password=account_info["password"]):
            print(f"Successfully logged in to account: {account_info['username']}")
            return bot
        else:
            print(f"Failed to log in to account: {account_info['username']}")
            return None
    except Exception as e:
        print(f"An error occurred while logging in to account {account_info['username']}: {e}")
        return None

def report_user(bot_instance, target_username, report_type="fake_account"):
    """
    Reports a specific user.
    report_type can be "fake_account", "spam", "violence", etc. (check instabot docs for details)
    """
    try:
        user_id = bot_instance.get_user_id_from_username(target_username)
        if user_id:
            if bot_instance.report_user(user_id, report_type=report_type):
                print(f"Successfully reported user {target_username} as {report_type}.")
                return True
            else:
                print(f"Failed to report user {target_username}.")
                return False
        else:
            print(f"User {target_username} not found.")
            return False
    except Exception as e:
        print(f"An error occurred while reporting user {target_username}: {e}")
        return False

def add_proxy():
    """Adds a new proxy to the list."""
    proxy = input("Enter new proxy (e.g., http://user:pass@ip:port): ").strip()
    if proxy and proxy not in proxies_data:
        proxies_data.append(proxy)
        print(f"Proxy added: {proxy}")
    elif proxy in proxies_data:
        print("This proxy already exists.")
    else:
        print("No valid proxy entered.")
    input("\nPress Enter to continue...")

def add_account():
    """Adds a new Instagram account."""
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    print("\nChoose a proxy for the account:")
    if not proxies_data:
        print("No proxies available. Account will be added without a proxy.")
        proxy_choice = ""
    else:
        for i, p in enumerate(proxies_data):
            print(f"{i+1}. {p}")
        print("0. Do not use proxy")
        try:
            choice = int(input("Enter the number of the proxy you want to use: "))
            if 1 <= choice <= len(proxies_data):
                proxy_choice = proxies_data[choice - 1]
            elif choice == 0:
                proxy_choice = ""
            else:
                print("Invalid choice. No proxy will be used.")
                proxy_choice = ""
        except ValueError:
            print("Invalid input. No proxy will be used.")
            proxy_choice = ""

    if username and password:
        accounts_data.append({
            "username": username,
            "password": password,
            "proxy": proxy_choice
        })
        print(f"Account added: {username} (Proxy: {proxy_choice if proxy_choice else 'None'})")
    else:
        print("Username and password are required to add an account.")
    input("\nPress Enter to continue...")

def start_report_with_filter(use_proxy_accounts_only):
    """
    Starts the reporting process based on whether the account uses a proxy or a local IP.
    :param use_proxy_accounts_only: True to report with proxy accounts only, False for local IP accounts only.
    """
    if not accounts_data:
        print("No accounts added to start the reporting process.")
        input("\nPress Enter to continue...")
        return

    target_account_to_report = input("Enter the username of the account you want to report: ").strip()
    if not target_account_to_report:
        print("No account specified for reporting. Operation cancelled.")
        input("\nPress Enter to continue...")
        return

    filtered_accounts = []
    if use_proxy_accounts_only:
        filtered_accounts = [acc for acc in accounts_data if acc["proxy"]]
        print("\nStarting report process using proxy accounts only...")
    else:
        filtered_accounts = [acc for acc in accounts_data if not acc["proxy"]]
        print("\nStarting report process using local IP accounts only...")

    if not filtered_accounts:
        print("No accounts matching the specified criteria.")
        input("\nPress Enter to continue...")
        return

    print(f"Reporting account: {target_account_to_report}")
    for account in filtered_accounts:
        print(f"\nAttempting to log in with account: {account['username']}")
        bot = login_and_control(account)
        if bot:
            report_user(bot, target_account_to_report, report_type="fake_account")
            time.sleep(5) # 5-second delay between each report operation
            # bot.logout() # Some libraries might require this or at the end of each operation
    print("\nReporting process finished.")
    input("\nPress Enter to continue...")

def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        clear_screen()
        print("BİXRepo")
        print("1. Start report with proxy (for accounts with proxy)")
        print("2. Start report with local IP (for accounts without proxy)")
        print("3. Add proxy")
        print("4. Add account")
        print("5. View added accounts and proxies")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            start_report_with_filter(True) # True means use proxy accounts only
        elif choice == '2':
            start_report_with_filter(False) # False means use local IP accounts only
        elif choice == '3':
            add_proxy()
        elif choice == '4':
            add_account()
        elif choice == '5':
            print("\n--- Added Accounts ---")
            if accounts_data:
                for acc in accounts_data:
                    print(f"Username: {acc['username']}, Proxy: {acc['proxy'] if acc['proxy'] else 'None'}")
            else:
                print("No accounts added.")
            print("\n--- Added Proxies ---")
            if proxies_data:
                for p in proxies_data:
                    print(p)
            else:
                print("No proxies added.")
            input("\nPress Enter to continue...")
        elif choice == '6':
            print("Exiting BİXRepo. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()

if __name__ == "__main__":
    main_menu()
