# Implementa protocolo binario: [4 bytes longitud] + JSON
import json, struct

def send_message(sock, obj):
    data = json.dumps(obj).encode("utf-8")
    sock.sendall(struct.pack(">I", len(data)) + data)

def _recv_all(sock, n):
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket cerrado")
        data.extend(chunk)
    return bytes(data)

def recv_message(sock):
    header = _recv_all(sock, 4)
    (length,) = struct.unpack(">I", header)
    payload = _recv_all(sock, length)
    return json.loads(payload.decode("utf-8"))
