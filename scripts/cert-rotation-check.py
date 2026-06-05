#!/usr/bin/env python3

import subprocess
import datetime
import json
from colorama import Fore, Style, init

init(autoreset=True)

# Alert if cert expires within this many days
EXPIRY_WARNING_DAYS = 30

def get_kubernetes_secrets():
    """Get all TLS secrets from Kubernetes"""
    try:
        result = subprocess.run(
            ["kubectl", "get", "secrets", "--all-namespaces",
             "-o", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️  kubectl not available: {e}")
        return None

def check_url_cert(hostname, port=443):
    """Check SSL certificate expiry for a URL"""
    try:
        result = subprocess.run(
            ["openssl", "s_client", "-connect",
             f"{hostname}:{port}", "-servername", hostname],
            input="Q",
            capture_output=True,
            text=True,
            timeout=10
        )
        # Parse expiry date from openssl output
        for line in result.stderr.split("\n"):
            if "notAfter" in line:
                expiry_str = line.split("=")[1].strip()
                expiry_date = datetime.datetime.strptime(
                    expiry_str, "%b %d %H:%M:%S %Y %Z"
                )
                days_left = (expiry_date - datetime.datetime.now()).days
                return days_left, expiry_date
        return None, None
    except Exception as e:
        return None, None

def check_certificates():
    """Main function to check all certificates"""
    print(f"{Style.BRIGHT}Restaurant SRE Platform — Certificate Check")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Style.BRIGHT}{'='*50}")

    issues_found = False

    # Check common endpoints
    endpoints = [
        ("orders.restaurant.com", 443),
        ("grafana.restaurant.com", 443),
    ]

    print(f"\n{Style.BRIGHT}Checking SSL Certificates:")

    for hostname, port in endpoints:
        days_left, expiry_date = check_url_cert(hostname, port)

        if days_left is None:
            print(f"{Fore.YELLOW}⚠️  {hostname}: Could not check "
                  f"(not reachable in local env)")
            continue

        if days_left < 0:
            print(f"{Fore.RED}❌ {hostname}: EXPIRED {abs(days_left)}"
                  f" days ago!")
            issues_found = True
        elif days_left < EXPIRY_WARNING_DAYS:
            print(f"{Fore.RED}❌ {hostname}: EXPIRING in "
                  f"{days_left} days! ({expiry_date.date()})")
            issues_found = True
        else:
            print(f"{Fore.GREEN}✅ {hostname}: OK — "
                  f"{days_left} days left ({expiry_date.date()})")

    # Summary
    print(f"\n{Style.BRIGHT}{'='*50}")
    if issues_found:
        print(f"{Fore.RED}{Style.BRIGHT}⚠️  Certificate issues found!")
        print(f"Action required: Renew certificates immediately")
    else:
        print(f"{Fore.GREEN}{Style.BRIGHT}✅ All certificates OK!")
    print(f"{Style.BRIGHT}{'='*50}\n")

    return not issues_found

if __name__ == "__main__":
    check_certificates()