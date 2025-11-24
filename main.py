# main.py
import os
from gtts import gTTS
from datetime import datetime
import time
import random
from moviepy.editor import VideoFileClip, AudioFileClip
from instagrapi import Client

# ==================== Config ====================
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
BACKGROUND_VIDEO = "tech_background.mp4"

# ==================== Login with Retry ====================
def login_instagram():
    client = Client()
    try:
        if os.path.exists("session.json"):
            client.load_settings("session.json")
            print("Session loaded")
        else:
            client.login(INSTA_USERNAME, INSTA_PASSWORD)
            client.dump_settings("session.json")
            print("Login successful")
        return client
    except Exception as e:
        print(f"Login error: {e}")
        return None

client = login_instagram()
if not client:
    print("Cannot login. Check username/password.")
    exit()

# ==================== Get Trend ====================
def get_trend():
    return random.choice(["هوش مصنوعی", "AI", "گجت", "تکنولوژی", "نوآوری"])

trend = get_trend()

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

# ==================== Create Voice ====================
ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
audio_file = f"audio_{ts}.mp3"

tts = gTTS(text=caption, lang='fa', slow=False)
tts.save(audio_file)

# ==================== Create Video ====================
video = VideoFileClip(BACKGROUND_VIDEO).subclip(0, 15)
audio = AudioFileClip(audio_file).set_duration(15)
final = video.set_audio(audio)
final.write_videofile(f"reel_{ts}.mp4", fps=24, codec="libx264", audio_codec="aac")

# ==================== Upload ====================
try:
    client.clip_upload(f"reel_{ts}.mp4", caption=caption)
    print(f"Reel uploaded successfully! {ts}")
except Exception as e:
    print(f"Upload error: {e}")

# ==================== Schedule ====================
while True:
    time.sleep(4 * 60 * 60)  # 4 hours
