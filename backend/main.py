from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from vid_sum import video_summarisation
import os
import cv2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI backend is running"}

@app.post("/process/")
async def process_video(file: UploadFile = File(...)):
    input_folder = "input"
    final_folder = "output"
    os.makedirs(final_folder, exist_ok=True)
    os.makedirs(input_folder, exist_ok=True)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_rate=30

    input_path = os.path.join(input_folder, file.filename)
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Process the video and get output path
    output_path = video_summarisation(input_path, fourcc, frame_rate)

    return FileResponse(output_path, media_type="video/mp4", filename=f"{os.path.splitext(file.filename)[0]}_new.mp4")
