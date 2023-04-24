# importing all required libraries
import sys,telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import requests
import streamlit as st


message = sys.argv[1]

BOT_API_KEY = st.secrets["telegram"]["BOT_API_KEY"]

response = requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage', {
    'chat_id': '-1001972403574',
    'text': message
})

if response.status_code == 200:
    print('ok')
else:
    print(response.text)  # Do what you want with response