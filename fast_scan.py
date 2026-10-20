import socket

target = "scanme.nmap.org"

print(f"[*] Starting automated scan on {target} (Ports 1-100)...")
print("[*] This might take a few seconds...")

# حلقة تكرار تفحص المنافذ من 1 إلى 100
for port in range(1, 101):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5) # الانتظار نصف ثانية فقط لكل منفذ (للسرعة)
    
    result = s.connect_ex((target, port))
    
    if result == 0:
        print(f"[+] Port {port} is OPEN")
        
    s.close()

print("[*] Scan complete.")
