import io
import zipfile

import pytest

from services.zip_service import ZipService


def dummy_frames():
    yield (1, b"first")
    yield (2, b"second")
    yield (10, b"tenth")


def test_create_zip_from_frames_contains_expected_files_and_contents():
    zip_bytes = ZipService.create_zip_from_frames(dummy_frames())
    buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(buffer, "r") as zipf:
        namelist = zipf.namelist()
        assert namelist == [
            "frame_0001.jpg",
            "frame_0002.jpg",
            "frame_0010.jpg",
        ]
        assert zipf.read("frame_0001.jpg") == b"first"
        assert zipf.read("frame_0002.jpg") == b"second"
        assert zipf.read("frame_0010.jpg") == b"tenth"


def test_create_zip_from_frames_empty_generator_returns_empty_zip():

    def empty_frames():
        if False:
            yield None

    zip_bytes = ZipService.create_zip_from_frames(empty_frames())
    buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(buffer, "r") as zipf:
        assert zipf.namelist() == []


def test_create_zip_from_frames_padding_of_frame_numbers():

    def single_frame():
        yield (123, b"data")

    zip_bytes = ZipService.create_zip_from_frames(single_frame())
    buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(buffer, "r") as zipf:
        namelist = zipf.namelist()
        assert namelist == ["frame_0123.jpg"]
        assert zipf.read("frame_0123.jpg") == b"data"
