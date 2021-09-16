#!/usr/bin/env python3
import socket, sys
import multiprocessing
import time

#define address & buffer size
HOST = "wwww.google.com"
PORT = 80
BUFFER_SIZE = 1024
PROXY_SERVER = "localhost"
PROXY_PORT = 8001

def respond(conn,s2):
    #recieve data from proxy_server
    client_data = conn.recv(BUFFER_SIZE)
    print("received data from proxy_client: ",client_data)
    
    #send data from proxy_client to www.goole.com
    s2.sendall(client_data)
    s2.shutdown(socket.SHUT_WR)

    #receive data from google.com
    #continue accepting data until no more left
    host_data = b""
    while True:
        data = s2.recv(BUFFER_SIZE)
        if not data:
            break
        host_data += data
    print("received data from www.google.com: ",host_data)

    #send google.com data to proxy_client
    conn.sendall(host_data)
    

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")


def main():
    #socket for connection between proxy_client and proxy_server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:

        #reuse the same binding port
        s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
        #bind socket to address
        s1.bind((PROXY_SERVER, PROXY_PORT))
        #set to listening mode
        s1.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s1.accept()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        
                #set up connection to google.com
                remote_ip = socket.gethostbyname( "www.google.com" )
                s2.connect((remote_ip , PORT))
                print (f'Socket Connected to {HOST} on ip {remote_ip}')
                    
                process = multiprocessing.Process(target=respond, args=(conn,s2),daemon = True)
                process.start()

            conn.close()
                


if __name__ == "__main__":
    main()
