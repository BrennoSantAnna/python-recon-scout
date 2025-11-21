import socket
import sys
import requests
import re
import subprocess
import platform
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def get_ip(domain):
    print(f"\n--- Resolving IP for {domain} ---")

    try:
        ip_address = socket.gethostbyname(domain)
        print(f"[*] IP address found: {ip_address}")
        return ip_address
    except socket.gaierror as e:
        print(f"[!] Could not resolve domain: {domain}. Error: {e}")
        return None
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")
        return None


def scan_ports(ip):
    print(f"\n--- Scanning Common Ports on {ip} ---")
    communs_ports = [21, 22, 25, 80, 110, 443, 8080, 8443]

    for port in communs_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"[*] Port {port} is OPEN!")

        except (socket.timeout, ConnectionRefusedError):
            pass
        except Exception as e:
            print(f"[!] Error scanning port {port}: {e}")
        finally:
            sock.close()

    print("--- Port Scann Finished ---")


def get_web_info(url):
    print(f"\n--- Analyzing Web Info for {url} ---")

    try:
        response_main = requests.get(url, timeout=5)
        
        server_header = response_main.headers.get("Server")
        if server_header:
            print(f"[*] Server Header: {server_header}")
        else:
            print(f"[-] Server Header not found.")

        robots_url = urljoin(url, "/robots.txt")
        response_robots = requests.get(robots_url, timeout=5)

        if response_robots.status_code == 200:
            print("[+] robots.txt found (showing first 5 lines):")

            robots_content = "\n".join(response_robots.text.split("\n")[:5])
            print(robots_content)
        else:
            print(f"[-] robots.txt not found (Status Code: {response_robots.status_code}).")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error during web info gathering: {e}")


def scrape_page(url):
    print(f"\n--- Scraping Page {url} ---")

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        print("\n[*] Finding Links...")
        soup = BeautifulSoup(response.text, "lxml")

        all_links = soup.find_all("a", href=True)

        if not all_links:
            print("[-] No links found on the page.")
        else:
            print(f"[+] Found {len(all_links)} total links.")
            for link_tag in all_links:
                full_url = urljoin(url, link_tag["href"])
                print(f"  - {full_url}")

        print("\n[*] Finding Emails...")
        email_pattern = r"([\w.-]+@[\w.-]+\.\w+)"
        emails = re.findall(email_pattern, response.text)

        if not emails:
            print("[-] No emails addresses on the page.")
        else:
            print(f"[+] Found {len(emails)} emails addresses.")
            for email in emails:
                print(f"  - {email}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error during web scraping: {e}")


def run_nmap_scan(ip):
    target_ip = ip
    print(f"[*] Performing a fast scan on top 100 ports for {ip}...")

    command = ['nmap', '-F', ip]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=300)

        print("\n--- Nmap Scan Results ---")
        print(result.stdout)

    except FileNotFoundError:
        print("[!] Error: 'nmap' command not found. Is Nmap installed and in your system's PATH?")
    except subprocess.CalledProcessError as e:
        print("[!] Host seems to be DOWN. Error:")
        print(e.stderr)
    except subprocess.TimeoutExpired:
        print("[!] Error: The Nmap scan timed out (more than 5 minutes).")


def main():
    if len(sys.argv) != 2:
        print("Usage: python recon_scout.py <domain.com>")
        sys.exit(1)

    target_domain = sys.argv[1]

    if not target_domain.startswith("http"):
        target_url = f"http://{target_domain}"
    else:
        target_url = target_domain
        target_domain = target_domain.replace("http://", "").replace("https://", "").split("/")[0]

    print(f"--- Starting Reconnaissance on {target_domain} ---")

    target_ip = get_ip(target_domain)

    if target_ip:
        scan_ports(target_ip)

    get_web_info(target_url)
    scrape_page(target_url)

    print("\n--- Reconnaissance Finished ---")


if __name__ == "__main__":
    main()
