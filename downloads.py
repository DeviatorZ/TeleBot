import requests
from settings import *
from yt_dlp import YoutubeDL
import os
import io

def getImage(imgUrl):
    try:
        response = requests.get(url=imgUrl)
    except:
        return False, "Request failed! Try again later..."
    
    if response.status_code != 200:
        return False, "Failed to download image"
    
    contentType = response.headers["Content-Type"].split("/")
    if contentType[0] == "image": 
        return True, response.content
    else:
        return False, "This URL doesn't contain an image!"
    
def getVideo(videoUrl, chatId):
    ydlOptions = {
        "format": "best[ext=mp4]",
        "max_filesize": MAX_VIDEO_SIZE,
        "outtmpl": f"{VIDEO_FOLDER}/{chatId}/%(title)s.%(ext)s",
        "noplaylist": True,
    }
    try:
        os.mkdir(f"{VIDEO_FOLDER}/{chatId}")
    except:
        pass

    with YoutubeDL(ydlOptions) as ydl:
        try:
            ydl.download(videoUrl)
        except:
            return False

    return True

def downloadedVideo(chatId):
    path = f"{VIDEO_FOLDER}/{chatId}"
    files = os.listdir(path)
    videoFiles = [f for f in files if f.endswith(".mp4")]
    videoStreams = []

    for videoFile in videoFiles:
        filePath = os.path.join(path, videoFile)
        with open(filePath, "rb") as filePointer:
            videoData = filePointer.read()
            videoStream = io.BytesIO(videoData)
            videoStream.name = videoFile
            videoStreams.append(videoStream)

        os.remove(filePath)

    return videoStreams
        