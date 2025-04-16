from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    Query,
    UploadFile,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.v1.validations.videos import check_video_size, check_video_type
from core.dependency_injection import Container
from core.security import verify_jwt
from schemas.user import User
from schemas.video import Video
from services.notification_service import NotificationService
from services.video_service import VideoService

router = APIRouter(prefix="/video")


@router.post("/upload", response_model=Video)
@inject
async def upload_video(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    video_service: VideoService = Depends(Provide[Container.video_service]),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    try:
        user = verify_jwt(auth.credentials)

        if not check_video_type(file):
            raise ValueError(
                f"File type '{file.content_type}' is not allowed."
            )
        if not check_video_size(file):
            raise ValueError("File size exceeds the limit of 10 MB")

        content = await file.read()
        user_id = user["id"]
        filename = f"videos/{user_id}/{file.filename}"
        video = video_service.save_video(file, filename, user["id"])
        if not video:
            raise HTTPException(status_code=400, detail="Failed to save video")

        background_tasks.add_task(
            video_service.upload_video, content, filename, video.id
        )

        background_tasks.add_task(
            video_service.process_video,
            content,
            video,
            user,
        )

        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e


@router.get("/", response_model=list[Video])
@inject
def list_videos(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1, le=100),
    video_service: VideoService = (Depends(Provide[Container.video_service])),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    user = verify_jwt(auth.credentials)
    user_id = user["id"]
    videos = video_service.list_videos(user_id, limit=limit, page=page)
    return videos
