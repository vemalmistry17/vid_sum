import os
import cv2
from PIL import Image
import imagehash
import numpy as np
from numpy.linalg import norm
import subprocess

def video_summarisation(video_path, fourcc, frame_rate):
  cap = cv2.VideoCapture(video_path)
  width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  frames = []
  hold = []
  sim = []
  count = 0
  while True:
    ret, frame = cap.read()
    if not ret or frame is None:
      break
    else:
      new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if len(frames) == 0:
      frames.append(frame)
      hold.append(new_frame)
    else:
      vec1 = hold[0]
      vec2 = new_frame
      h1 = imagehash.average_hash(Image.fromarray(vec1))
      h2 = imagehash.average_hash(Image.fromarray(vec2))
      ham_dist = h1 - h2
      if ham_dist > 1:
        frames.append(frame)
      hold[0] = vec2
      sim.append(ham_dist)
    count += 1
  cap.release()

  # Create a temporary directory to store the frames
  temp_dir = "temp_frames"
  os.makedirs(temp_dir, exist_ok=True)

  # Save the frames as images
  for i, frame in enumerate(frames):
    cv2.imwrite(os.path.join(temp_dir, f"frame_{i:04d}.png"), frame)

  # Use ffmpeg to create the video
  new_vid = os.path.join("output", f"{os.path.splitext(os.path.basename(video_path))[0]}_new.mp4")
  ffmpeg_cmd = [
      "ffmpeg",
      "-r", str(frame_rate),
      "-i", os.path.join(temp_dir, "frame_%04d.png"),
      "-c:v", "libx264",
      "-pix_fmt", "yuv420p",
      "-y",
      new_vid
  ]
  subprocess.run(ffmpeg_cmd)

  # Clean up the temporary directory
  for file_name in os.listdir(temp_dir):
      os.remove(os.path.join(temp_dir, file_name))
  os.rmdir(temp_dir)

  return new_vid
