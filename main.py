# main.py
from gtts import gTTS
from datetime import datetime
import time
import random
from moviepy.editor import VideoFileClip, AudioFileClip
from instagrapi import Client
import os

# ==================== Login with Session Only ====================
cl = Client()
cl.delay_range = [1, 5]  # ضد بن

if not os.path.exists("session.json"):
    print("ERROR: session.json not found! Upload it to GitHub.")
    exit()

cl.load_settings("session.json")
try:
    cl.get_timeline_feed()  # تست اتصال بدون پسورد
    print("Session loaded successfully! Logged in without password")
except Exception as e:
    print("Session expired or invalid:", e)
    print("Delete session.json and login again locally.")
    exit()

# ==================== Get Trend ====================
trend = random.choice(["هوش مصنوعی", "AI", "گجت", "تکنولوژی", "نوآوری"])

# ==================== Generate Caption ====================
captions = [
    f"همین الان {trend} داره دنیا رو تغییر میده! تو هنوز منتظری؟ #هوش_مصنوعی #AI #تکنولوژی #نوآوری",
    f"اگه از {trend} استفاده نکنی، ۱۰ سال عقب می‌مونی! #هوش_مصنوعی #AI #گجت #آینده",
    f"{trend} دیگه یه رویا نیست، الان اینجاست! #AI #تکنولوژی #نوآوری #گجت",
    f"سال ۲۰۳۰ همه با {trend} کار می‌کنن... تو چی؟ #هوش_مصنوعی #AI #آینده",
    f"خبر فوری: {trend} همه چیز رو عوض کرد! #هوش_مصنوعی #تکنولوژی #نوآوری #AI"
]

caption = random.choice(captions)
print(f"Caption: {caption}")

# ==================== Create Voice + Video ====================
ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
audio_file = f"audio_{ts}.mp3"
video_output = f"reel_{ts}.mp4"

# TTS
tts = gTTS(text=caption, lang='fa', slow=False)
tts.save(audio_file)

# Video
background = VideoFileClip("tech_background.mp4").subclip(0, 15)
audio = AudioFileClip(audio_file).set_duration(15)
final = background.set_audio(audio)
final.write_videofile(video_output, fps=24, codec="libx264", audio_codec="aac")

# ==================== Upload to Instagram ====================
try:
    cl.clip_upload(video_output, caption=caption)
    print(f"REEL UPLOADED SUCCESSFULLY! {ts} 🚀")
except Exception as e:
    print("Upload failed:", e)

# ==================== Schedule (every 4 hours) ====================
print("Bot is running... Next reel in 4 hours.")
while True:
    time.sleep(4 * 60 * 60)  # ۴ ساعت صبر کن
