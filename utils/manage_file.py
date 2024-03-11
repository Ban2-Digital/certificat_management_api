import os
import random
import aiofiles
from fastapi import UploadFile
from settings.config import *

async def save_upload_file(upload_file: UploadFile, upload_to: str):
    try:
        # Create a unique filename
        filename = upload_file.filename
        print(filename)
        file_path = os.path.join(MEDIA_ROOT, upload_to, filename)
        base_path = os.path.join(MEDIA_ROOT, upload_to)
        print("file_path before while loop", file_path)
        print("file_path before while loop exist", os.path.exists(file_path))
        # Check if the file already exists
        while os.path.exists(file_path):
            # Generate a random 7-digit number
            random_number = random.randint(1000000, 9999999)
            # Append the random number to the filename
            file_path = os.path.join(MEDIA_ROOT, upload_to, f"{random_number}_{filename}")
            print("file_path in while loop", file_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print("after check the dir")
        
        # Save the file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await upload_file.read()  # read the file
            print("out_file", out_file)
            # print("content", content)
            await out_file.write(content)  # write the file

        file_url = os.path.join(MEDIA_URL, upload_to, os.path.basename(file_path)).replace("\\", "/")

        return file_url

    except Exception as e:
        print(e)
        return ""


# async 
def delete_file(file_path):
    base_path = BASE_DIR
    list_path = str(file_path).split('/')
    
    # try:
    #     async with aiofiles.open(file_path, 'wb') as file:
    #         content = ""
    #         await content 
    # except Exception as e:
    #     print(e)
    #     return e
    
delete_file(file_path="medias/formations/ebook-bg.png")