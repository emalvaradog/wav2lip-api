import os

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pyngrok import ngrok
import nest_asyncio

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

preset = "fast"

@app.get("/")
def read_root():
  return {"status": "ok", "message": "Hello World"}


@app.post("/sync")
def lip_sync(audio: UploadFile=File(...), video: UploadFile=File(...)):
  if (audio.filename.find(".wav") == -1):
    return {"status": "failed", "message": "Audio should be .wav"}

  else:
    audio_path = os.path.join("./sample_data", audio.filename)
    with open(audio_path, "wb") as f:
      f.write(audio.file.read())
      f.close()

    video_path = os.path.join("./sample_data", video.filename)
    with open(video_path, "wb") as f:
      f.write(video.file.read())
      f.close()

    video_path_name = './sample_data/%s' %(video.filename)
    audio_path_name = './sample_data/%s' %(audio.filename)
    

    print(video_path_name)
    print(audio_path_name)

    pad_top =  0
    pad_bottom =  25
    pad_left =  -10
    pad_right =  -10
    rescaleFactor =  1


    os.system("cd Wav2Lip && python3 interference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face '%s' --audio '%s' --pads %d %d %d %d --rescale_factor %d" %(video_path_name, audio_path_name, pad_top, pad_bottom, pad_left, pad_right, rescaleFactor))
    

    # !cd Wav2Lip 
    # !python inference.py --checkpoint_path checkpoints/wav2lip_gan.pth --face '../sample_data/1.mp4' --audio '../sample_data/2.wav' --pads $pad_top $pad_bottom $pad_left $pad_right

    result_path = "/Wav2Lip/results/result_voice.mp4"
    try:
      with open(result_path, "rb") as f:
        if f.file:
          size = os.stat(result_path)
          print(size.st_size)
          return FileResponse("./Wav2Lip/results/result_voice.mp4")
        else: 
          pass
    except:
      return {"status": "failed", "message": "Something went wrong"}



if __name__ == "__main__":
  PORT = 8000
  ngrok_tunnel = ngrok.connect(PORT)
  print("Public URL: ", ngrok_tunnel.public_url)
  nest_asyncio.apply()
  uvicorn.run(app, host="127.0.0.1", port=PORT)