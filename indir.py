import requests
import argparse
from os import system
import sys
import platform

os = platform.system()
if os == "Windows":
    clear = "cls"
    slash = "\\"
else:
    clear = "clear"
    slash = "/"

ap = argparse.ArgumentParser(description='BTK Akademi Video Indirici')
ap.add_argument("-u", "--url", help="Video url'i")
ap.add_argument("-f", "--file", help="Birden fazla video url'i içeren dosya")
ap.add_argument("-o", "--output", help="Dosyanın kaydedileceği konum")
args = vars(ap.parse_args())

def download(url, output):        
    video_id = url.split("/")[-1].split("?")[0]
    json_file = requests.get(f"https://cinema8.com/api/v1/uscene/rawvideo/flavor/{video_id}").json()
    with open(output+json_file["name"], "wb") as f:
        print("{} --> Indiriliyor...".format(json_file["name"]))
        f.write(requests.get(json_file["url"]).content)
        system(clear)
                
if len(sys.argv) == 1:
    ap.print_help()
    sys.exit()    

if args["file"] != None and args["url"] != None:
    print("Tek bir video mu, birden fazla mı?\nKarar ver!")
    sys.exit()
    
if args["output"] != None:
    if args["output"][-1] != slash:
        args["output"] += slash        
    output = args["output"]

if args["output"] == None:
    output = ""
            
if args["file"] != None:
    with open(args["file"], "r", encoding="utf-8") as file:
        for i in file.read().split("\n"):
            if len(i) == 0:
                continue
            download(i, output)
            
if args["url"] != None:
    download(args["url"], output)            