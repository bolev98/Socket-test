import socket
from time import sleep
import socketinfo
import threading as coroutine

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socketinfo.HOST, socketinfo.PORT))

is_active = True
count_recentRequests = 0

print(f"Connected to [{socketinfo.HOST}:{socketinfo.PORT}]")
print("Write /help for the list of commands.")

# def checkForDeath():
#     try:
#         data = client.recv(16)
#     except ConnectionResetError:
#         print("[DEBUG]: Looks like this socket unexpectedly closed")
#         return True

def spamPrevent_thread():
    global count_recentRequests
    while is_active:
        if count_recentRequests > 0:
            count_recentRequests -= 1
        sleep(1)

def listenForOutcome():
    global count_recentRequests
    global is_active
    while is_active:
        msg = input()
        match msg:
            case "/help":
                print('List of the current commands: \n/quit - disconnect from the chat."')
            case _:
                if count_recentRequests < socketinfo.spamPreventStrictness:
                    try:
                        client.send(msg.encode())
                        count_recentRequests += 1
                    except ConnectionResetError:
                        print("Unexpected fatal error.")
                        is_active = False
                        break
                else:
                    print("You are sending messages too quickly! Stop or I'll burn your internet adapter.")

        if msg == "/quit":
            print("Successfully left from the group.")
            is_active = False

def listenForIncome():
    global is_active
    while is_active:
        try:
            message = client.recv(1024).decode()
            print(message)
        except ConnectionResetError:
            print("Unexpected fatal error.")
            is_active = False
            break

coroutine.Thread(target=listenForIncome).start() #Income (sent by others) messages handler
coroutine.Thread(target=listenForOutcome).start() #Outcoming (sent) messages handler
coroutine.Thread(target=spamPrevent_thread).start() #Initialize to prevent spamming