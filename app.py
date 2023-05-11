from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil
import uuid
import uvicorn
import os 

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1]  # get file extension
    file_id = str(uuid.uuid4())  # generate random file id
    file_location = f"uploads/{file_id}{extension}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    return JSONResponse(content={"filename": file.filename, "fileId": file_id, "fileLocation": f"/uploads/{file_id}{extension}"})


@app.get("/uploads/{file_id:path}")
async def read_file(file_id: str):
    file_location = f"uploads/{file_id}"
    if not os.path.isfile(file_location):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_location)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)