from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import json

app = FastAPI(title="Telegram Video WebApp")

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Пути к файлам
current_dir = os.path.dirname(os.path.abspath(__file__))
webapp_dir = os.path.join(current_dir, "../webapp")
data_file = os.path.join(current_dir, "videos.json")

# Пример данных видео
sample_videos = [
    {
        "id": 1,
        "title": "Big Buck Bunny",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "description": "Большой кролик Бак"
    },
    {
        "id": 2,
        "title": "Elephant Dream", 
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "description": "Слон в мечтах"
    },
    {
        "id": 3,
        "title": "For Bigger Blazes",
        "url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "description": "Для больших вспышек"
    }
]

# Создаем файл с видео если его нет
def init_videos_file():
    if not os.path.exists(data_file):
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(sample_videos, f, ensure_ascii=False, indent=2)

# Раздаем статические файлы
app.mount("/static", StaticFiles(directory=webapp_dir), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(webapp_dir, "index.html"))

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Server is running"}

@app.get("/api/videos", response_model=List[dict])
async def get_videos():
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)
        return videos
    except FileNotFoundError:
        return sample_videos

@app.get("/api/videos/{video_id}")
async def get_video(video_id: int):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)
        
        video = next((v for v in videos if v["id"] == video_id), None)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video
    except FileNotFoundError:
        video = next((v for v in sample_videos if v["id"] == video_id), None)
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return video

@app.post("/api/videos")
async def add_video(video: dict):
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            videos = json.load(f)
    except FileNotFoundError:
        videos = sample_videos.copy()
    
    # Генерируем новый ID
    new_id = max([v["id"] for v in videos]) + 1 if videos else 1
    video["id"] = new_id
    videos.append(video)
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    
    return {"message": "Video added", "video": video}

# Инициализируем файл с видео при запуске
@app.on_event("startup")
async def startup_event():
    init_videos_file()