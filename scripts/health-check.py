#!/usr/bin/env python3

import requests
import subprocess
import datetime
import os
from colorama import Fore, Style, init

# Initialize colorama for colors
init(autoreset=True)

# Configuration
ORDER_SERVICE_URL = "http://localhost:3000"
PROMETHEUS_URL = "http://localhost:9090"
LOG_FILE = "logs/health-check.log"
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 85

def log(message):
    """Write message to log file with timestamp"""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    with open(LOG_FILE, "a") as f:
        f.write(log_message + "\n")
    print(log_message)

def check_order_service():
    """Check if order service is healthy"""
    print(f"\n{Style.BRIGHT}Checking Order Service...")
    try:
        response = requests.get(
            f"{ORDER_SERVICE_URL}/health", 
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print(f"{Fore.GREEN}✅ Order Service: HEALTHY")
                log("CHECK PASSED: order-service is healthy")
                return True
        print(f"{Fore.RED}❌ Order Service: UNHEALTHY")
        log("CHECK FAILED: order-service returned non-healthy status")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Order Service: DOWN - Connection refused")
        log("CHECK FAILED: order-service is down - connection refused")
        return False
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}❌ Order Service: TIMEOUT - Taking too long")
        log("CHECK FAILED: order-service timed out")
        return False

def check_prometheus():
    """Check if Prometheus is healthy"""
    print(f"\n{Style.BRIGHT}Checking Prometheus...")
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/-/healthy",
            timeout=5
        )
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Prometheus: HEALTHY")
            log("CHECK PASSED: prometheus is healthy")
            return True
        print(f"{Fore.RED}❌ Prometheus: UNHEALTHY")
        log("CHECK FAILED: prometheus returned non-200 status")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Prometheus: DOWN")
        log("CHECK FAILED: prometheus is down")
        return False

def check_metrics_endpoint():
    """Check if metrics endpoint is working"""
    print(f"\n{Style.BRIGHT}Checking Metrics Endpoint...")
    try:
        response = requests.get(
            f"{ORDER_SERVICE_URL}/metrics",
            timeout=5
        )
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ Metrics Endpoint: WORKING")
            log("CHECK PASSED: metrics endpoint is working")
            return True
        print(f"{Fore.RED}❌ Metrics Endpoint: FAILING")
        log("CHECK FAILED: metrics endpoint returned non-200")
        return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Metrics Endpoint: DOWN")
        log("CHECK FAILED: metrics endpoint is down")
        return False

def auto_remediate_order_service():
    """Automatically restart order service if down"""
    print(f"\n{Fore.YELLOW}🔧 Attempting auto-remediation...")
    log("REMEDIATION: attempting to restart order-service")
    try:
        result = subprocess.run(
            ["docker-compose", "restart", "order-service"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(f"{Fore.GREEN}✅ Auto-remediation successful!")
            log("REMEDIATION SUCCESS: order-service restarted")
            return True
        else:
            print(f"{Fore.RED}❌ Auto-remediation failed!")
            log(f"REMEDIATION FAILED: {result.stderr}")
            return False
    except Exception as e:
        print(f"{Fore.RED}❌ Auto-remediation error: {e}")
        log(f"REMEDIATION ERROR: {e}")
        return False

def print_summary(results):
    """Print a color coded summary table"""
    print(f"\n{Style.BRIGHT}{'='*50}")
    print(f"{Style.BRIGHT}HEALTH CHECK SUMMARY")
    print(f"{Style.BRIGHT}{'='*50}")
    
    all_healthy = True
    for check, status in results.items():
        if status:
            print(f"{Fore.GREEN}✅ {check:<30} HEALTHY")
        else:
            print(f"{Fore.RED}❌ {check:<30} UNHEALTHY")
            all_healthy = False
    
    print(f"{Style.BRIGHT}{'='*50}")
    if all_healthy:
        print(f"{Fore.GREEN}{Style.BRIGHT}Overall Status: ALL SYSTEMS HEALTHY")
        log("SUMMARY: All systems healthy")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}Overall Status: ISSUES DETECTED")
        log("SUMMARY: Issues detected - check logs")
    print(f"{Style.BRIGHT}{'='*50}\n")
    
    return all_healthy

def main():
    print(f"{Style.BRIGHT}Restaurant SRE Platform — Health Check")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log("=== Health Check Started ===")

    results = {}

    # Run all checks
    order_service_healthy = check_order_service()
    results["Order Service"] = order_service_healthy

    # Auto remediate if order service is down
    if not order_service_healthy:
        remediated = auto_remediate_order_service()
        if remediated:
            # Check again after remediation
            import time
            time.sleep(5)
            results["Order Service"] = check_order_service()

    results["Prometheus"] = check_prometheus()
    results["Metrics Endpoint"] = check_metrics_endpoint()

    # Print summary
    all_healthy = print_summary(results)

    log("=== Health Check Complete ===")

    # Exit code 1 if any issues found
    exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()