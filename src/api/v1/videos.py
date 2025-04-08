from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.dependency_injection import Container
from core.security import verify_jwt
from schemas.video import Video
from services.video_service import VideoService

router = APIRouter(prefix="/video")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Video)
@inject
async def convert_video(
    file: UploadFile = File(...),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    video_service: VideoService = (Depends(Provide[Container.video_service])),
):
    user = verify_jwt(auth.credentials)

    try:
        if not file.content_type.startswith("video/"):
            raise ValueError("File is not a valid video format")
        if file.size > 10 * 1024 * 1024:  # 10 MB limit
            raise ValueError("File size exceeds the limit of 10 MB")
        video = await video_service.save_video(file, user["id"])
        if not video:
            raise HTTPException(status_code=400, detail="Failed to save video")
        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e
