import socket
from typing import Iterable
import threading as coroutine
import socketinfo
import misc.debug_vars as debug_vars

active_sockets: dict[socket.socket] = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socketinfo.HOST, socketinfo.PORT))
print(f"[SETUP]: This server is located on port {socketinfo.PORT}")
print("[SETUP]: Listening for incoming clients...")

server.listen()

def ServerAnnouncement(content: str):
    for socket in active_sockets.values():
        socket.send(content.encode())

def ReplicateMessage(sender: socket.socket, content: str, address):
    parsed_message = f"[{address[1]}]: {content}"
    for socket in active_sockets.values():
        if socket != sender:
            socket.send(parsed_message.encode())

def listenForIncomingMessage(client, address):
    # global debug_vars
    while True:
        try:
            message = client.recv(1024).decode()
        except ConnectionAbortedError:
            if debug_vars.printSoftShutInfo:
                print(f"[DEBUG] [{address[1]}]: Force-disconnected.")
            break
        except ConnectionResetError:
            if debug_vars.printSoftShutInfo:
                print(f"[DEBUG] [{address[1]}]: Force-disconnected.")
            break
        if debug_vars.printRecievedMessages:
            print(f"[DEBUG] [CLIENT {address[1]}]: {message}")
        match message:
            case "/quit":
                active_sockets[address[1]].close()
                del active_sockets[address[1]]
                ServerAnnouncement(f"User {address[1]} left from the chat. Y'all are too boring...")
                print(f"[CONNECTION]: Removed [{address[1]}]")
                break
            case _:
                ReplicateMessage(client, message, address)

def listenForIncomingClients():
    while True:
        client, address = server.accept()
        active_sockets[address[1]] = client
        print(f"[CONNECTION]: Connected [{address[0]}:{address[1]}]")
        coroutine.Thread(target=listenForIncomingMessage, args=(client, address)).start()

def debug_funcs():
    global debug_vars
    while True:    
        command = input()
        match command.upper():
            case "CLIENTS":
                print("[SERVER]: Currently connected clients: "+" ".join(map(str, active_sockets.keys())))
            case "DC ALL":
                print("[SERVER]: Disconnected: " + " ".join(map(str, active_sockets.keys())))
                for socket in active_sockets.values():
                    socket.close()
                active_sockets.clear()
            case "DEBUG PRINT_RECIEVED":
                debug_vars.printRecievedMessages = not debug_vars.printRecievedMessages
                print("[SERVER]: All recieved messages will be printed here." 
                      if debug_vars.printRecievedMessages else
                      "[SERVER]: Messages won't be printed here." )
            case "DEBUG PRINT_SOFTSHUT":
                    debug_vars.printSoftShutInfo = not debug_vars.printSoftShutInfo
                    print("[SERVER]: All unexpected shutdowns will be announced here." 
                      if debug_vars.printSoftShutInfo else
                      "[SERVER]: Unexpected shutdowns won't be announced anymore." )

coroutine.Thread(target=debug_funcs).start()
listenForIncomingClients()