from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    file_id = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String)
    created_at = Column(DateTime, nullable=False)
