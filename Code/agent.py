from re import T
import socket
from time import sleep
import os
import psutil
import json

IP = socket.gethostbyname("localhost")
PORT = 5578
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")

            connected = True
            numberOfMsg = 1
            while connected:
        
                pid = os.getpid()
                python_process = psutil.Process(pid)
                memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB
                myMetrics = {
                    'currentProccessRAM: ': memoryUse,
                    'RAM usage: ':psutil.virtual_memory()[2],
                    'CPU usage: ': psutil.cpu_percent(4),
                    'CPU interrupts: ':  psutil.cpu_stats()[1]
                }

                # Serializing json  
                msg = json.dumps(myMetrics)      

                #send message   
                client.send(msg.encode(FORMAT))
                print("Message "+str(numberOfMsg)+" sent to server.")
                numberOfMsg += 1

                sleep(5)
        except Exception as e:
            print(e)
            print("server connection failed ! Do you want to connect again ? y/n")
            pm = input()
            if(pm=="n"):
                break
            else:
                continue

if __name__ == "__main__":
    main()
    