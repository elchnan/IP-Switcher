#!/usr/bin/python
import time
import subprocess
import netifaces as ni

def get_current_ip(interface='eth0'):
    try:
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        return ip
    except ValueError:
        print("Unable to find IP address for the given interface")
        return None

def scan_network(ip_class):
    available_ip = None
    for i in range(1, 255):
        ip_address = f"{ip_class}.{i}"
        if subprocess.run(["ping", "-c", "1", ip_address], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 1:
            available_ip = ip_address
            break
    return available_ip

def change_ip(new_ip):
    try:
        subprocess.run(["sudo", "ifconfig", "eth0", new_ip])
        print("IP address successfully changed")
        subprocess.run(["sudo", "ifconfig", "eth0", "down"])
        subprocess.run(["sudo", "ifconfig", "eth0", "up"])
        print("Network interface reset successfully")
    except Exception as e:
        print(f"An error occurred while changing the IP address: {e}")

def get_interval():
    while True:
        try:
            interval = int(input("Please enter the IP change interval in minutes: "))
            return interval
        except ValueError:
            print("Please enter a numeric value")
def main():
    print("""
   _____ _            _       _     
  / ____| |          | |     | |    
 | |    | | __ _  ___| | __ _| |__  
 | |    | |/ _` |/ __| |/ _` | '_ \ 
 | |____| | (_| | (__| | (_| | | | |
  \_____|_|\__,_|\___|_|\__, |_| |_|
                          __/ |      
                         |___/       
              IP Switcher V 1.1
    """)
    
    interval = get_interval()
    current_ip = get_current_ip()
    ip_class = current_ip.rsplit('.', 1)[0]  # Extracting IP class
    print(f"Current IP address: {current_ip}")
    while True:
        new_ip = scan_network(ip_class)
 #       print(f"Scanning network for available IP address in class {ip_class}")
        if new_ip:
            change_ip(new_ip)
#            print(f"The new IP address is: {new_ip} (Time: {time.strftime('%H:%M:%S', time.localtime())})")
        else:
            print("No available IP address found")
        time.sleep(interval * 60)  # Sleep for the specified interval in minutes

if __name__ == "__main__":
    main()



