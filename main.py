from telegram.ext import *
from settings import API_KEY
from commands import *

def main():
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", startCommand))
    app.add_handler(CommandHandler("help", helpCommand))
    app.add_handler(CommandHandler("img", imgCommand))
    app.add_handler(CommandHandler("video", videoCommand))

    app.run_polling()
    
if __name__ == "__main__":
    main()