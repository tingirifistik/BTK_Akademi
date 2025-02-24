import requests
from yt_dlp import YoutubeDL
from os import system
from time import sleep

ACCESS_TOKEN = ""
BASE_URL = "https://www.btkakademi.gov.tr/api/service/v1"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0", "Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json, text/plain, */*", "Content-Type": "application/json"}

def register_course(course_id):
    url = f"{BASE_URL}/course/registration/register/{course_id}?language=tr"
    response = requests.post(url, headers=HEADERS, json={"demandForm": {}})
    return response.json().get("status", "Error")

def get_syllabus(course_id):
    url = f"{BASE_URL}/public/51/course/details/program/syllabus/{course_id}?language=tr"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def select_option(options, prompt):
    for index, option in enumerate(options, start=1):
        print(f"{index}- {option['title']}")
    choice = int(input(f"\n{prompt}: ")) - 1
    return choice

def start_lesson(course_id, lesson_id):
    url = f"{BASE_URL}/course/deliver/start/{lesson_id}"
    response = requests.post(url, headers=HEADERS, json={"programId": int(course_id)})
    return response.json().get("remoteCourseReference", "")

def get_video_url(video_id):
    url = f"https://cinema8.com/api/v1/uscene/rawvideo/flavor/{video_id}"
    response = requests.get(url).json()
    return response.get("name", "video.mp4"), response.get("hlsUrl", "")

def download_video(video_name, video_url):
    if not video_url:
        print("Video URL bulunamadı!")
        return
    output_template = video_name.replace(".mp4", "") + ".mp4"
    with YoutubeDL({'outtmpl': output_template}) as ydl:
        print(f"{video_name} indiriliyor...\n")
        ydl.download([video_url])

course_url = input("Kurs URL: ")
course_id = course_url.split("-")[-1]
system("cls||clear")
print("Kursa kaydolma durumu: ", register_course(course_id))
sleep(1.5)
system("cls||clear")

syllabus = get_syllabus(course_id)
section_index = select_option(syllabus, "Bölüm seçin")
system("cls||clear")

lesson_index = select_option(syllabus[section_index]["courses"], "Ders seçin")
lesson_id = str(syllabus[section_index]["courses"][lesson_index]["id"])
system("cls||clear")

video_id = start_lesson(course_id, lesson_id)
if not video_id:
    print("ACCESS_TOKEN eksik veya geçersiz!")
    sleep(2)
    exit()
    
video_name, video_url = get_video_url(video_id)
download_video(video_name, video_url)

