from telegram.ext import *
from telegram import Update
from utils import isValidUrl
from downloads import getImage, getVideo, downloadedVideo
from settings import MAX_VIDEO_UPLOAD_TIME

async def startCommand(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Use /help command to get started!")

async def helpCommand(update : Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="/img {URL} - downloads an image from a given URL.\n/video {URL} - downloads a video from a given URL if it's under 50MB in size.")

async def handleArgCount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    argCount = len(context.args)

    if argCount == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Add a URL when using this command!")
        return True
    elif argCount > 1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Only one URL at a time!")
        return True
    
    return False
    
async def imgCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await handleArgCount(update, context):
        return
    chatId = update.effective_chat.id
    imgUrl = context.args[0]

    if not isValidUrl(imgUrl):
        await context.bot.send_message(chat_id=chatId, text="Invalid URL!")
        return
    imageObtained, data = getImage(imgUrl)

    if imageObtained:
        await context.bot.send_photo(chat_id=chatId, photo=data)
    else:
        await context.bot.send_message(chat_id=chatId, text=data)  


async def videoCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await handleArgCount(update, context):
        return
    chatId = update.effective_chat.id
    videoUrl = context.args[0]

    if not isValidUrl(videoUrl):
        await context.bot.send_message(chat_id=chatId, text="Invalid URL!")
        return
    
    await context.bot.send_message(chat_id=chatId, text="Getting video...")
    gotVideo = getVideo(videoUrl, chatId)
    if not gotVideo:
        await context.bot.send_message(chat_id=chatId, text="Something went wrong during download!")

    downloaded = downloadedVideo(chatId)
    if len(downloaded) > 0:
        await context.bot.send_message(chat_id=chatId, text="Sending video...")

        for video in downloaded:
            await context.bot.send_document(chat_id=chatId, document=video, read_timeout=MAX_VIDEO_UPLOAD_TIME) 

        await context.bot.send_message(chat_id=chatId, text="Video sent!")
    else:
        await context.bot.send_message(chat_id=chatId, text="Couldn't get a video!")
