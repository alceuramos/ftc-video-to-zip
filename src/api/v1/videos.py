from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.dependency_injection import Container
from core.security import verify_jwt
from core.settings import settings
from schemas.video import Video
from services.video_service import VideoService

router = APIRouter(prefix="/video")


@router.post("/upload")
@inject
async def upload_video(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    video_service: VideoService = Depends(Provide[Container.video_service]),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        user = verify_jwt(auth.credentials)
        allowed_video_types = [
            "video/mp4",
            "video/mkv",
            "video/avi",
            "video/mov",
            "video/quicktime",
        ]
        if file.content_type not in allowed_video_types:
            raise ValueError(
                f"File type '{file.content_type}' is not allowed. Allowed types: {', '.join(allowed_video_types)}"
            )
        if file.size > 10 * 1024 * 1024:  # 10 MB limit
            raise ValueError("File size exceeds the limit of 10 MB")

        content = await file.read()
        user_id = user["id"]
        filename = f"videos/{user_id}/{file.filename}"
        video = video_service.save_video(file, filename, user["id"])
        if not video:
            raise HTTPException(status_code=400, detail="Failed to save video")

        background_tasks.add_task(
            video_service.upload_to_s3, content, filename, video.id
        )

        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e
