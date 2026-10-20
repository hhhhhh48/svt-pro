import socket

# هدفنا سيكون خادم التدريب الذي فحصناه سابقاً (المنفذ 22 مفتوح)
target = "scanme.nmap.org"
port = 22

print(f"[*] Connecting to {target}:{port}...")

# إنشاء اتصال
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(3) # الانتظار 3 ثواني كحد أقصى

try:
    s.connect((target, port))
    # استقبال البيانات (حتى 1024 بايت)
    banner = s.recv(1024)
    print("[+] Banner received:")
    print(banner.decode('utf-8', errors='ignore').strip())
except Exception as e:
    print(f"[-] Error: {e}")
finally:
    s.close()
