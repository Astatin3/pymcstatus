import io
import math
import base64
import sys
import re
import PIL
from time import sleep
from threading import Thread
from PIL import Image
import operator
from collections import defaultdict
from mcstatus import JavaServer

imgsize = (16,16)
sleeptime = 0.1

nullimg = b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAaklEQVQ4T62TWw7AIAgEl/sf2qoRY4ywa1tD/JvhoRjGKUAN/RhQY1y3sKdpEltht2Z17Mmm4A3cW3AjE+yVTk4RnNqUBdGMJEE2YCpgr5MKGNymHwoUOBSo8FGw/j72J1LBDfzPMn1d5wfNZUf5qKNxAQAAAABJRU5ErkJggg=="

def img2ascii(icon):

    img = Image.open(io.BytesIO(base64.b64decode(icon)))
    img = img.resize(imgsize)
    imageSizeW, imageSizeH = img.size

    asciiimg = []
    for i in range(0, imageSizeW):
        curline = ""
        for j in range(0, imageSizeH):
            pixVal = img.getpixel((j, i))

            # if len(pixVal) != 4 or pixVal[3] == 0:
            #     symbol = "  "
            # else:
            #     symbol = "██"
            
            curline += (f"\033[38;2;{pixVal[0]};{pixVal[1]};{pixVal[2]}m██")


            #curline += colored(symbol, curcolor[3])
        asciiimg.append(curline+"\033[38;2;255;255;255m > ")
    return asciiimg



def scanip(ip):
    try:
        #print(f"Scanning IP: {ip}")
        server = JavaServer.lookup(ip)
        status = server.status()
    except:
        #print(f"Error: {ip}")
        return False

    #print(status.icon)

    if status.icon == None:
        b64img = nullimg
    else:
        b64img = status.icon[22:]

    ascii = img2ascii(b64img)
    ver = status.version
    players = status.players

    motdtxt = status.motd.to_plain()

    motd = ["", ""]
    if "\n" in motdtxt:
        split = motdtxt.split("\n")
        motd[0] = split[0]
        motd[1] = split[1]
    else:
        motd[0] = motdtxt

    for ln in range(0,imgsize[1],1):
        line = ascii[ln]
        match ln:
            case 0:
                line += f"IP: {ip}"
            case 1:
                line += f"Latency: {math.ceil(status.latency)}ms"
            case 2:
                line += f"P: {ver.protocol}, V: {ver.name}"
            case 3:
                line += f"{players.online}/{players.max} Players"
            case 5:
                line += f"{motd[0]}"
            case 6:
                line += f"{motd[1]}"

        print(line)
    print("\n")
    return True

threads = []

if sys.argv[1] == "-p":
    if not scanip(sys.argv[2]):
        print("Server not online")
elif sys.argv[1] == "-f":

    with open(sys.argv[2]) as file:
        for ip in file:
            #print(f"Scanning IP: {ip}")
            thread = Thread(target = scanip, args = (ip.strip(), ))
            thread.start()
            threads.append(thread)
            sleep(sleeptime)

    scanip(sys.argv[1])

    for thread in threads:
        thread.join()
else:
    print("Usage:\n"+\
          "srvstatus.py -p IP\n"+\
          "srvstatus.py -f FILE")
