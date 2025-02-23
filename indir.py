import requests
from yt_dlp import YoutubeDL
from os import system
from time import sleep

ACCESS_TOKEN = ""

def kurs_kayit(course_id):
    url = f"https://www.btkakademi.gov.tr/api/service/v1/course/registration/register/{course_id}?language=tr"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json={"demandForm": {}})
    return r.json().get("status", "Error")

def liste1(course_id):
    url = f"https://www.btkakademi.gov.tr/api/service/v1/public/51/course/details/program/syllabus/{course_id}?language=tr"
    headers = {"User-Agent": "Mozilla/5.0", "Authorization": f"Bearer {ACCESS_TOKEN}"}
    r = requests.get(url, headers=headers)
    return r.json()

def sec(options, prompt):
    for index, option in enumerate(options, start=1):
        print(f"{index}- {option['title']}")
    choice = int(input(f"\n\n{prompt}: "))
    return choice - 1

def liste2(course_id, lesson_id):
    url = f"https://www.btkakademi.gov.tr/api/service/v1/course/deliver/start/{lesson_id}"
    headers = {"User-Agent": "Mozilla/5.0", "Authorization": f"Bearer {ACCESS_TOKEN}"}
    r = requests.post(url, headers=headers, json={"programId": int(course_id)})
    return r.json().get("remoteCourseReference", "")

def video_url(video_id):
    session = requests.Session()
    url = f"https://cinema8.com/api/v1/uscene/rawvideo/flavor/{video_id}"
    r = session.get(url).json()
    return r.get("name", "video.mp4"), r.get("hlsUrl", "")

def download_video(video_name, video_url):
    if not video_url:
        print("Video URL bulunamadı!")
        return
    output_template = video_name.split(".mp4")[0] + ".mp4"
    with YoutubeDL({'outtmpl': output_template}) as ydl:
        print(f"{video_name} indiriliyor...\n")
        ydl.download([video_url])

if __name__ == "__main__":
    kurs_url = input("Kurs URL: ")
    kurs_id = kurs_url.split("-")[-1]
    system("cls||clear")
    print("Kursa kaydolma durumu: ", kurs_kayit(kurs_id))
    sleep(1.5)
    system("cls||clear")
    syllabus = liste1(kurs_id)
    bolum = sec(syllabus, "Bölüm seçin")
    system("cls||clear")
    ders_sec = sec(syllabus[bolum]["courses"], "Ders seçin")
    ders_id = str(syllabus[bolum]["courses"][ders_sec]["id"])
    system("cls||clear")
    video_id = liste2(kurs_id, ders_id)
    if not video_id:
        print("ACCESS_TOKEN eksik veya geçersiz!")
        sleep(2)
        exit()
    video_name, video_url = video_url(video_id)
    download_video(video_name, video_url)