import socket
import threading
import json
from prometheus_client import Gauge,start_http_server

IP = socket.gethostbyname("localhost")
PORT = 5578
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

metric1 = Gauge('process_ram_usage_percent', 'usage of my ram',['agent_number'])
metric2 = Gauge('process_cpu_usage_percent', 'usage of my cpu in 4 seconds',['agent_number'])
metric3 = Gauge('process_ram_gigabytes', 'usage of my ram in current proccess',['agent_number'])
metric4 = Gauge('process_cpu_interrupts_total', 'number of cpu interrupts since boot',['agent_number'])

def handle_client(conn, addr,number):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)

        print(f"[{addr}] {msg}")
        metricsFromClient = json.loads(msg)

        metrics = []
        metrics.append(metricsFromClient['RAM usage: '])
        metrics.append(metricsFromClient['CPU usage: '])
        metrics.append(metricsFromClient['currentProccessRAM: '])
        metrics.append(metricsFromClient['CPU interrupts: '])

        metric1.labels("agent_" + str(number)).set(metrics[0])
        metric2.labels("agent_" + str(number)).set(metrics[1])
        metric3.labels("agent_" + str(number)).set(metrics[2])
        metric4.labels("agent_" + str(number)).set(metrics[3])

    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()

    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    number = 1
    start_http_server(8001)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr,number))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {number}")
        number += 1

if __name__ == "__main__":
    main()