import socket
import sys

# عنوان الهدف (سنفحص هاتفك أو أي جهاز في الشبكة)
target = "192.168.10.39" # يمكنك تغييره إلى 192.168.10.1 لفحص الراوتر

# المنافذ الشهيرة التي نريد فحصها
ports = [21, 22, 23, 53, 80, 443, 8080]

print(f"[*] Starting scan on target: {target}")

for port in ports:
    # إنشاء اتصال TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1) # الانتظار لثانية واحدة فقط
    
    # محاولة الاتصال بالمنفذ
    result = s.connect_ex((target, port))
    
    if result == 0:
        print(f"[+] Port {port} is OPEN")
    else:
        print(f"[-] Port {port} is closed or filtered")
    
    s.close()

print("[*] Scan complete.")
