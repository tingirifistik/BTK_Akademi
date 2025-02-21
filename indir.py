from requests import get, post, session
from os import system
from time import sleep
from yt_dlp import YoutubeDL

ACCESS_TOKEN = ""

url = input("Url: ")
kurs = url.split("-")[-1]

system("cls||clear")

url = f"https://www.btkakademi.gov.tr:443/api/service/v1/course/registration/register/{kurs}?language=tr"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "Authorization": "Bearer "+ACCESS_TOKEN, "Origin": "https://www.btkakademi.gov.tr", "Dnt": "1", "Referer": "", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers", "Connection": "close"}
json={"demandForm": {}}
print(post(url, headers=headers, json=json).json()["status"])

sleep(1)
system("cls||clear")

url = f"https://www.btkakademi.gov.tr:443/api/service/v1/public/51/course/details/program/syllabus/{kurs}?language=tr"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Authorization": "Bearer "+ACCESS_TOKEN, "Dnt": "1", "Referer": "", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers", "Connection": "close"}
r = get(url, headers=headers).json()

x = 0
while 1: 
    try:
        print(str(x+1)+"- "+r[x]["title"])
    except IndexError:
        break
    x+=1
sec = int(input("\n\nSeçim: "))

system("cls||clear")

x = 0
while 1:
    try:
        print(str(x+1)+"- "+r[sec-1]["courses"][x]["title"]) 
    except IndexError:
        break
    x+=1
sec2 = int(input("\n\nSeçim: "))
id = str(r[sec-1]["courses"][sec2-1]["id"])

system("cls||clear")

url = "https://www.btkakademi.gov.tr:443/api/service/v1/course/deliver/start/"+id
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "*/*", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Referer": "", "Content-Type": "application/json", "Authorization": "Bearer "+ACCESS_TOKEN, "Origin": "https://www.btkakademi.gov.tr", "Dnt": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin", "Te": "trailers", "Connection": "close"}
json={"programId": int(kurs)}
try:
    video_id = post(url, headers=headers, json=json).json()["remoteCourseReference"]
except:
    print("ACCESS_TOKEN eksik!!")
    sleep(2)
    exit()

oturum = session()
url = f"https://cinema8.com:443/raw-video/{video_id}?c=js-api&sub=tr&t=s0"
cookies = {"JSESSIONID": "31E6BD18E17DEA8137079E9954B99008.jvm4"}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate, br", "Dnt": "1", "Referer": "", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "iframe", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "cross-site", "Te": "trailers", "Connection": "close"}
oturum.get(url, headers=headers, cookies=cookies)

json_file = oturum.get(f"https://cinema8.com/api/v1/uscene/rawvideo/flavor/{video_id}").json()
with YoutubeDL({'outtmpl': json_file["name"].split(".mp4")[0]+'.mp4'}) as ydl:
    print("{} --> Indiriliyor...".format(json_file["name"].split(".mp4")[0])+"\n\n")
    ydl.download(json_file["hlsUrl"])