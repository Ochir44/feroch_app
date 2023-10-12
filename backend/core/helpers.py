import os
import uuid

import aiofiles
from fastapi import UploadFile


async def handle_file_upload(file: UploadFile) -> str:
    """This function serves media files"""

    # Separates file name and its format
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join("../backend/media")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if content:
        # Hashes the file name and write its in directory - img_dir
        file_name = f"{uuid.uuid4().hex}{ext}"
        async with aiofiles.open(os.path.join(img_dir, file_name), mode="wb") as f:
            await f.write(content)

        return file_name
    else:
        return 0
