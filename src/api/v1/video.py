from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import verify_jwt
from core.video_upload_s3 import S3StorageService
from schemas.video import Video

router = APIRouter(prefix="/video")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Video)
async def convert_video(
    file: UploadFile = File(...),
    auth: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    user = verify_jwt(auth.credentials)

    try:
        contents = await file.read()
        url = S3StorageService().upload_file(
            contents,
            file.filename,
            file.content_type,
            user_id=user["id"],
        )
        video = Video(
            file_path=url,
            user_id=user["id"],
            title=file.filename,
            status="processing",
        )
        return video
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error"
        ) from e
