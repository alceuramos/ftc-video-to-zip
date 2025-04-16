from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from src.db.postgresql.database import Base


class Video(Base):
    __tablename__ = "videos"
    __table_args__ = {"extend_existing": True}

    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    zip_path = Column(String, nullable=True)
    status = Column(String, nullable=True, default="processing")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    id = Column(Integer, primary_key=True, index=True)
