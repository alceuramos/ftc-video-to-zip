from fastapi import UploadFile


def check_video_size(file: UploadFile) -> bool:
    return file.size < (10 * 1024 * 1024 * 1024)  # 10 MB


def check_video_type(file: UploadFile) -> bool:
    return file.content_type in [
        "video/mp4",
        "video/mkv",
        "video/avi",
        "video/mov",
        "video/quicktime",
    ]
