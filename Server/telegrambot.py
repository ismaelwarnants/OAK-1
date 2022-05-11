import telegram

# Docs: https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html
# Source: https://usp-python.github.io/06-bot/#sending-a-message-part-1

api_key = "5347368126:AAGs3plNlDPqF9i057CDpT3rVLXv5AQFlSA"
user_id = "619833245"

bot = telegram.Bot(token=api_key)

def send_message(message):
    bot.send_message(chat_id=user_id, text=message)

def send_video(video_path):
    # Source: https://stackoverflow.com/questions/47615956/send-video-through-telegram-python-api
    bot.send_video(chat_id=user_id, video=open(video_path, 'rb'), supports_streaming=True)

def main():
    send_message("YESSSSS")
    send_video("/home/ismael/Documents/test.mp4")

if __name__ == '__main__':
    main()