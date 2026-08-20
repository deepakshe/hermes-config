import os
import sys
import time
import requests
import argparse
import asyncio
import urllib.parse
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

# Force stdout/stderr to UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

try:
    from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
except ImportError:
    print("Error: moviepy is not installed correctly.")
    sys.exit(1)

import edge_tts
from instagrapi import Client

load_dotenv()

# Curated high-impact GitHub Repositories for instant rich content
REPO_DATABASE = {
    "ollama": {
        "name": "ollama / ollama",
        "stars": "115k ⭐",
        "tagline": "Run Llama 3 & DeepSeek locally on your PC",
        "command": "ollama run deepseek-r1:8b",
        "pros": ["100% Free & Open Source", "Complete Data Privacy (No Cloud)", "One-command terminal execution"],
        "cons": ["Requires at least 16GB RAM / GPU", "Command-line interface by default"],
        "desc_hindi": "yeh tool aapke computer pe bina internet aur bina API key ke, top AI models jaise DeepSeek aur Llama 3 ko local run karta hai."
    },
    "open-webui": {
        "name": "open-webui / open-webui",
        "stars": "68k ⭐",
        "tagline": "ChatGPT UI clone for Local LLMs",
        "command": "docker run -d -p 3000:8080 open-webui",
        "pros": ["Sleek ChatGPT-like Dark Interface", "Supports Voice Chat, RAG & Web Search", "Self-hosted & Multi-user"],
        "cons": ["Requires Docker to run easily", "Needs moderate setup for beginners"],
        "desc_hindi": "yeh aapke local models ko ek poora ChatGPT jaisa sundar web interface deta hai, jismein documents chat aur web search bhi shamil hai."
    },
    "comfyui": {
        "name": "comfyanonymous / ComfyUI",
        "stars": "62k ⭐",
        "tagline": "Most powerful node-based AI Image & Video generator",
        "command": "python main.py --highvram --listen",
        "pros": ["Ultimate control over AI generation", "Extremely fast and memory efficient", "Huge community of custom nodes"],
        "cons": ["Steep learning curve (Node graph UI)", "Needs dedicated NVIDIA GPU (6GB+ VRAM)"],
        "desc_hindi": "yeh duniya ka sabse powerful open-source AI image aur video generator hai, jisse studios high quality cinematic content banate hain."
    },
    "vllm": {
        "name": "vllm-project / vllm",
        "stars": "38k ⭐",
        "tagline": "High-throughput and lightning-fast LLM serving engine",
        "command": "vllm serve meta-llama/Llama-3-8B-Instruct",
        "pros": ["PagedAttention for 24x faster speed", "Handles hundreds of users concurrently", "Production-grade inference"],
        "cons": ["Designed specifically for Linux servers", "Requires dedicated GPU setup"],
        "desc_hindi": "yeh LLM inference ko 24 guna zyada fast bana deta hai, jisse companies apne production apps mein AI models host karti hain."
    }
}

def get_repo_data(topic):
    topic_lower = topic.lower()
    for key, data in REPO_DATABASE.items():
        if key in topic_lower or data["name"].lower() in topic_lower:
            return data
    # Fallback to Ollama if not directly matched
    return REPO_DATABASE["ollama"]

def generate_hindi_script(repo_data):
    name = repo_data["name"]
    desc = repo_data["desc_hindi"]
    cmd = repo_data["command"]
    pros = ", ".join(repo_data["pros"])
    cons = ", ".join(repo_data["cons"])
    
    script_segments = [
        f"Agar aap ek programmer ya AI enthusiast hain, toh yeh GitHub repository aapka ghanto ka kaam minutes mein kar degi! Iska naam hai {name}.",
        f"Yeh tool karta kya hai? Dhyan se suniye. {desc}. Isko execute karna behad aasan hai, bas terminal mein likhiye: '{cmd}', aur yeh instantly start ho jayega.",
        f"Ab baat karte hain iske sabse bade pros yaani faaydo ki! Pehla: {repo_data['pros'][0]}. Doosra: {repo_data['pros'][1]}. Aur teesra: {repo_data['pros'][2]}.",
        f"Lekin kuch cons aur limitations ka dhyan zaroor rakhein. Jaise ki: {repo_data['cons'][0]}, aur {repo_data['cons'][1]}.",
        "Toh agar aapko yeh open-source repository pasand aayi, toh video ko save aur share kar lo, aur rozana best AI tools ke liye follow zaroor karo!"
    ]
    
    full_script = " ".join(script_segments)
    return full_script, script_segments

async def generate_hindi_voiceover_async(text, output_path):
    print(f"[TTS] Generating Hindi voiceover with hi-IN-MadhurNeural...")
    communicate = edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="+3%", pitch="+0Hz")
    await communicate.save(output_path)
    print(f"[TTS] Hindi voiceover saved: {output_path}")

def generate_voiceover(text, output_path):
    asyncio.run(generate_hindi_voiceover_async(text, output_path))

def create_scene_image(scene_type, repo_data, subtitle_text, output_path, w=1080, h=1920):
    canvas = Image.new("RGB", (w, h), (13, 17, 23)) # GitHub dark background
    draw = ImageDraw.Draw(canvas)
    
    # Fonts setup
    font_bold_path = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_reg_path = "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(font_bold_path): font_bold_path = "arial.ttf"
    if not os.path.exists(font_reg_path): font_reg_path = "arial.ttf"
    
    title_font = ImageFont.truetype(font_bold_path, 60)
    header_font = ImageFont.truetype(font_bold_path, 44)
    body_font = ImageFont.truetype(font_reg_path, 36)
    sub_font = ImageFont.truetype(font_bold_path, 40)
    
    # Top GitHub Header Bar
    draw.rectangle([0, 0, w, 140], fill=(22, 27, 34))
    draw.text((60, 45), "🐙 GITHUB REPO SHOWCASE", fill=(88, 166, 255), font=header_font)
    draw.text((w - 240, 45), repo_data["stars"], fill=(227, 179, 65), font=header_font)
    
    # Scene Specific Rendering
    if scene_type == 0:  # Hook / Main Repo Card
        # Main Card Box
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(22, 27, 34), outline=(48, 54, 61), width=3)
        draw.text((100, 320), "FEATURED REPOSITORY", fill=(139, 148, 158), font=body_font)
        draw.text((100, 400), repo_data["name"], fill=(88, 166, 255), font=title_font)
        draw.text((100, 520), repo_data["tagline"], fill=(240, 246, 252), font=header_font)
        
        # Open-source Badge
        draw.rounded_rectangle([100, 720, 460, 810], radius=16, fill=(35, 134, 54))
        draw.text((130, 745), "⚡ 100% OPEN SOURCE", fill=(255, 255, 255), font=body_font)
        
    elif scene_type == 1:  # Terminal Execution Demo
        # Terminal Box
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(1, 4, 9), outline=(48, 54, 61), width=3)
        # Terminal Header with 3 dots
        draw.rounded_rectangle([60, 260, w - 60, 340], radius=24, fill=(22, 27, 34))
        draw.ellipse([90, 285, 115, 310], fill=(248, 81, 73))   # red
        draw.ellipse([130, 285, 155, 310], fill=(227, 179, 65)) # yellow
        draw.ellipse([170, 285, 195, 310], fill=(46, 160, 67))  # green
        draw.text((230, 280), "Terminal / CLI Execution", fill=(139, 148, 158), font=body_font)
        
        # Terminal Command lines
        draw.text((100, 400), "$ git clone https://github.com/" + repo_data["name"].replace(" ", ""), fill=(139, 148, 158), font=body_font)
        draw.text((100, 480), "$ " + repo_data["command"], fill=(63, 185, 80), font=header_font)
        draw.text((100, 600), ">>> Initializing local environment...", fill=(201, 209, 217), font=body_font)
        draw.text((100, 670), ">>> Model loaded in VRAM (0.8s) 🚀", fill=(88, 166, 255), font=body_font)
        draw.text((100, 740), ">>> Ready for prompt execution!", fill=(46, 160, 67), font=body_font)

    elif scene_type == 2:  # Pros / Faayde
        draw.text((60, 220), "🔥 TOP ADVANTAGES & PROS", fill=(46, 160, 67), font=title_font)
        y = 330
        for pro in repo_data["pros"]:
            draw.rounded_rectangle([60, y, w - 60, y + 160], radius=20, fill=(22, 27, 34), outline=(46, 160, 67), width=2)
            draw.text((100, y + 50), f"✅ {pro}", fill=(240, 246, 252), font=header_font)
            y += 200

    elif scene_type == 3:  # Cons / Limitations
        draw.text((60, 220), "⚠️ LIMITATIONS & CONS", fill=(248, 81, 73), font=title_font)
        y = 330
        for con in repo_data["cons"]:
            draw.rounded_rectangle([60, y, w - 60, y + 180], radius=20, fill=(22, 27, 34), outline=(248, 81, 73), width=2)
            draw.text((100, y + 60), f"❌ {con}", fill=(240, 246, 252), font=header_font)
            y += 220

    elif scene_type == 4:  # Outro / CTA
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(22, 27, 34), outline=(88, 166, 255), width=3)
        draw.text((120, 350), "🚀 WANT THE REPO LINK?", fill=(240, 246, 252), font=title_font)
        draw.text((120, 480), "💬 Comment 'REPO' below", fill=(88, 166, 255), font=header_font)
        draw.text((120, 580), "📥 Link will be sent in DM", fill=(139, 148, 158), font=body_font)
        draw.rounded_rectangle([120, 700, w - 120, 830], radius=20, fill=(31, 111, 235))
        draw.text((160, 740), "✨ FOLLOW FOR DAILY AI REPOS", fill=(255, 255, 255), font=header_font)

    # Bottom Subtitle Box (Hinglish/Hindi Subtitles)
    box_w = 980
    box_h = 320
    box_x = (w - box_w) // 2
    box_y = h - box_h - 120
    
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=(1, 4, 9, 230), outline=(88, 166, 255), width=3)
    
    # Word wrap subtitles
    words = subtitle_text.split()
    lines = []
    curr_line = []
    for word in words:
        test = " ".join(curr_line + [word])
        try:
            bbox = draw.textbbox((0, 0), test, font=sub_font)
            lw = bbox[2] - bbox[0]
        except AttributeError:
            lw = len(test) * 20
        if lw <= 880:
            curr_line.append(word)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [word]
    if curr_line:
        lines.append(" ".join(curr_line))
        
    sub_y = box_y + 40
    for line in lines[:4]: # at most 4 lines
        try:
            bbox = draw.textbbox((0, 0), line, font=sub_font)
            lw = bbox[2] - bbox[0]
        except AttributeError:
            lw = len(line) * 20
        sx = (w - lw) // 2
        draw.text((sx + 2, sub_y + 2), line, fill=(0, 0, 0), font=sub_font)
        draw.text((sx, sub_y), line, fill=(255, 223, 0), font=sub_font)
        sub_y += 55
        
    canvas.save(output_path)

def zoom_frame(frame, t, duration, zoom_ratio=0.05):
    h, w, c = frame.shape
    scale = 1.0 + zoom_ratio * (t / duration)
    pil_img = Image.fromarray(frame)
    new_w, new_h = int(w * scale), int(h * scale)
    pil_resized = pil_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return np.array(pil_resized.crop((left, top, left + w, top + h)))

def build_60s_video(repo_data, script_segments, audio_path, output_mp4_path):
    print("[VIDEO] Compiling 5-scene 60s Hindi GitHub Reel with MoviePy...")
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    
    words_per_seg = [len(s.split()) for s in script_segments]
    total_words = sum(words_per_seg)
    
    clips = []
    temp_frames = []
    
    try:
        for i, segment in enumerate(script_segments):
            ratio = words_per_seg[i] / total_words
            seg_duration = ratio * total_duration
            frame_path = f"temp_scene_{i}.png"
            create_scene_image(i, repo_data, segment, frame_path)
            temp_frames.append(frame_path)
            
            img_clip = ImageClip(frame_path).with_duration(seg_duration)
            zoomed_clip = img_clip.transform(lambda gf, t, dur=seg_duration: zoom_frame(gf(t), t, dur))
            clips.append(zoomed_clip)
            
        video_concat = concatenate_videoclips(clips, method="compose").with_audio(audio_clip)
        video_concat.write_videofile(output_mp4_path, fps=24, codec="libx264", audio_codec="aac", logger="bar")
        print(f"[VIDEO] Video compiled successfully at {output_mp4_path} (Duration: {total_duration:.1f}s)")
    finally:
        for clip in clips:
            try: clip.close()
            except: pass
        try: video_concat.close()
        except: pass
        try: audio_clip.close()
        except: pass
        for f in temp_frames:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

def main():
    parser = argparse.ArgumentParser(description="Automated 1-Minute Hindi GitHub Video Generator")
    parser.add_argument("--topic", type=str, default="ollama", help="GitHub repo name or keyword")
    parser.add_argument("--output", type=str, help="Output MP4 file path")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Skip Instagram upload")
    
    args = parser.parse_args()
    
    repo_data = get_repo_data(args.topic)
    print(f"==================================================")
    print(f" Generating 1-Min Hindi Video for: {repo_data['name']} ")
    print(f"==================================================")
    
    full_script, segments = generate_hindi_script(repo_data)
    
    downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    temp_audio = os.path.join(downloads_dir, 'temp_hindi_voice.mp3')
    output_mp4 = args.output or os.path.join(downloads_dir, 'output_reel.mp4')
    
    try:
        generate_voiceover(full_script, temp_audio)
        build_60s_video(repo_data, segments, temp_audio, output_mp4)
        
        hashtags = f"#github #coding #developer #ai #programming #hindi #tech #opensource #{args.topic.replace('-', '').lower()}"
        caption = f"Top GitHub Repo: {repo_data['name']} 🚀\n\n{full_script}\n\n{hashtags}"
        
        print(f"\n=========================================")
        print(f"1-MINUTE HINDI GITHUB REEL READY!")
        print(f"File Path: {output_mp4}")
        print(f"Suggested Caption:\n{caption}")
        print(f"=========================================")
    finally:
        if os.path.exists(temp_audio):
            try: os.remove(temp_audio)
            except: pass

if __name__ == "__main__":
    main()
