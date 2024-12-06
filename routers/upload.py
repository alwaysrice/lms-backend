import cloudinary
from fastapi import APIRouter, File, UploadFile
from decouple import config

app = APIRouter(
    tags=["upload"]
)
CLOUD_NAME = config("CLOUD_NAME")
CLOUD_API_KEY = config("CLOUD_API_KEY")
CLOUD_API_SECRET = config("CLOUD_API_SECRET")
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=CLOUD_API_KEY,
    api_secret=CLOUD_API_SECRET
)

from cloudinary.uploader import upload, destroy
import cloudinary.api
import cloudinary.uploader

@app.post("/upload/new")
async def upload_file(file: UploadFile = File(...)):
    try:
        print("Try uplaodding....")
        # content = await file.read();
        result = upload(file.file, resource_type="auto")
        print("result: ", result)
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
    except Exception as e:
        print("Error: " + str(e))
        return {
            "error": str(e)
        }


@app.post("/upload/replace/{id}")
async def replace_file(id: str, file: UploadFile = File(...)):
    try:
        destroy_result = destroy(id)
        if destroy_result.get("result") != "ok":
            return {
                "error": "Fail"
            }
        result = cloudinary.uploader.upload(file.file, resource_type="auto")
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }
    except Exception as e:
        return {
            "error": str(e)
        }


@app.delete("/upload/remove/{id}")
async def remove_file(id: str):
    try:
        destroy_result = destroy(id)
        if destroy_result.get("result") == "ok":
            return {
                "message": "Good"
            }
        return {
            "error": "Fail"
        }
    except Exception as e:
        return {
            "error": str(e)
        }
