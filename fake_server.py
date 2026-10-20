import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 9999)) # يعمل على هاتفك فقط
server.listen(1)

print("[*] Fake Server is running on port 9999...")

while True:
    conn, addr = server.accept()
    conn.send(b"Enter Password: ")
    password = conn.recv(1024).decode().strip()
    
    if password == "algeria2024":
        conn.send(b"Access Granted! Welcome Hacker.")
    else:
        conn.send(b"Access Denied!")
    conn.close()
