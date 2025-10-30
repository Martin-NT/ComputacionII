# client.py 
# Cliente TCP de prueba para servidor B
import socket
from common.protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 9090

with socket.create_connection((HOST, PORT)) as sock:
    send_message(sock, {"task": "analyze", "url": "https://example.com"})
    resp = recv_message(sock)
    print(resp["status"], list(resp.get("processing_data", {}).keys()))
