import os
from dotenv import load_dotenv
load_dotenv()



bot_token = os.getenv('BOT_TOKEN')
admin_channel_chat_id = os.getenv('ADMIN_CHANNEL_CHAT_ID')