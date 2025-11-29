from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uuid, os, shutil, datetime
from . import models, database

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Telegram Video WebApp Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Only video files allowed")

    ext = os.path.splitext(file.filename)[1]
    file_id = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, file_id)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    video = models.Video(
        file_id=file_id,
        filename=file.filename,
        content_type=file.content_type,
        created_at=datetime.datetime.utcnow()
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    return {"status": "ok", "file_id": file_id}

@app.get("/videos")
def videos(db: Session = Depends(get_db)):
    arr = db.query(models.Video).order_by(models.Video.created_at.desc()).all()
    return [
        {
            "id": v.id,
            "file_id": v.file_id,
            "filename": v.filename,
            "url": f"/uploads/{v.file_id}",
            "created_at": v.created_at.isoformat()
        }
        for v in arr
    ]

@app.get("/video/{file_id}")
def serve_file(file_id: str):
    fp = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(fp):
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(fp)
