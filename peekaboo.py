import socket
import sys
from datetime import datetime
import asyncio
import nmap

print("""
   ▄███████▄    ▄████████    ▄████████    ▄█   ▄█▄    ▄████████ ▀█████████▄   ▄██████▄   ▄██████▄  
  ███    ███   ███    ███   ███    ███   ███ ▄███▀   ███    ███   ███    ███ ███    ███ ███    ███ 
  ███    ███   ███    █▀    ███    █▀    ███▐██▀     ███    ███   ███    ███ ███    ███ ███    ███ 
  ███    ███  ▄███▄▄▄      ▄███▄▄▄      ▄█████▀      ███    ███  ▄███▄▄▄██▀  ███    ███ ███    ███ 
▀█████████▀  ▀▀███▀▀▀     ▀▀███▀▀▀     ▀▀█████▄    ▀███████████ ▀▀███▀▀▀██▄  ███    ███ ███    ███ 
  ███          ███    █▄    ███    █▄    ███▐██▄     ███    ███   ███    ██▄ ███    ███ ███    ███ 
  ███          ███    ███   ███    ███   ███ ▀███▄   ███    ███   ███    ███ ███    ███ ███    ███ 
 ▄████▀        ██████████   ██████████   ███   ▀█▀   ███    █▀  ▄█████████▀   ▀██████▀   ▀██████▀  
                                         ▀                                                         """)

async def scan_port(target, port):
    try:
        conn = await asyncio.open_connection(target, port)
        print(f"[*] Port {port} is open")
        conn[1].close()
        await conn[1].wait_closed()
    except asyncio.TimeoutError:
        print(f"[-] Timeout on port {port}")
    except ConnectionRefusedError:
        print(f"[-] Connection refused on port {port}")
    except OSError as e:
        print(f"[-] OSError on port {port}: {e}")

async def main(target, start_port, end_port):
    tasks = []
    for port in range(start_port, end_port + 1):
        tasks.append(scan_port(target, port))
    
    await asyncio.gather(*tasks)

def fingerprint_services(target, open_ports):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-sV -p ' + ','.join(map(str, open_ports)))
    for host in nm.all_hosts():
        print(f'Nmap scan report for {host}')
        for proto in nm[host].all_protocols():
            print(f'Protocol: {proto}')
            ports = nm[host][proto].keys()
            for port in ports:
                print(f'Port: {port}\tService: {nm[host][proto][port]["name"]}\tVersion: {nm[host][proto][port]["version"]}')

print("""Welcome to Peekaboo!
""")

target = input("What is the target IP? ")

start_port = int(input("What is the start port? "))
end_port = int(input("What is the end port? "))

print("-" * 50)
print("Target IP: " + target)
print("Scanning started at: " + str(datetime.now()))
print("This may take awhile...")
print("-" * 50)

try:
    asyncio.run(main(target, start_port, end_port))

except KeyboardInterrupt:
    print("Exiting Peekaboo")
    sys.exit()

except socket.error as e:
    print(f"The target IP is not responding: {e}")
    sys.exit()

print("Scanning completed at: " + str(datetime.now()))
