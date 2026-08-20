import os
import sys
import time
import argparse
import asyncio
import urllib.parse
import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips
import edge_tts
import requests

def fetch_live_github_info(repo_name):
    if "/" not in repo_name:
        repo_name = f"popular/{repo_name}"
    clean_name = repo_name.strip()
    url = f"https://api.github.com/repos/{clean_name}"
    try:
        r = requests.get(url, headers={"User-Agent": "AntigravityAgent"}, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return {
                "name": data.get("full_name", repo_name),
                "stars": f"{data.get('stargazers_count', 0):,} ⭐",
                "tagline": data.get("description") or "Open source developer tool",
                "command": f"git clone https://github.com/{data.get('full_name', repo_name)}.git",
                "pros": ["100% Free & Open Source", "Active community maintenance", "Zero subscription fees"],
                "cons": ["Requires technical setup", "Hardware dependent"],
                "desc_hindi": f"yeh ek behtareen open source tool hai jo {data.get('description', 'coding aur AI')} ke liye kaam aata hai."
            }
    except Exception as e:
        print(f"[WARN] Live fetch failed: {e}")
    
    # Fallback template
    return {
        "name": repo_name,
        "stars": "Top ⭐",
        "tagline": "Open Source AI & Developer Repository",
        "command": f"git clone https://github.com/{repo_name}.git",
        "pros": ["100% Free & Open Source", "Complete Data Privacy", "Lightweight & Fast"],
        "cons": ["CLI Interface", "Moderate hardware requirement"],
        "desc_hindi": "yeh ek powerful GitHub tool hai jo aapke development workflow ko 10 guna fast bana deta hai."
    }

def generate_hindi_script(repo_data):
    name = repo_data["name"]
    desc = repo_data["desc_hindi"]
    cmd = repo_data["command"]
    
    script_segments = [
        f"Agar aap ek programmer ya AI enthusiast hain, toh yeh GitHub repository aapka ghanto ka kaam minutes mein kar degi! Iska naam hai {name}.",
        f"Yeh tool karta kya hai? Dhyan se suniye. {desc}. Isko execute karna behad aasan hai, bas terminal mein likhiye: '{cmd}', aur yeh instantly start ho jayega.",
        f"Ab baat karte hain iske sabse bade pros yaani faaydo ki! Pehla: {repo_data['pros'][0]}. Doosra: {repo_data['pros'][1]}. Aur teesra: {repo_data['pros'][2]}.",
        f"Lekin kuch limitations ka dhyan zaroor rakhein. Jaise ki: {repo_data['cons'][0]}, aur {repo_data['cons'][1]}.",
        "Toh agar aapko yeh open-source repository pasand aayi, toh video ko save aur share kar lo, aur rozana best AI tools ke liye follow zaroor karo!"
    ]
    return " ".join(script_segments), script_segments

async def generate_tts(text, out_path, voice="hi-IN-MadhurNeural"):
    comm = edge_tts.Communicate(text, voice)
    await comm.save(out_path)

def create_scene(idx, repo_data, subtitle, out_path, w=1080, h=1920):
    canvas = Image.new("RGB", (w, h), (13, 17, 23))
    draw = ImageDraw.Draw(canvas)
    
    font_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_reg = "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(font_bold): font_bold = "arial.ttf"
    if not os.path.exists(font_reg): font_reg = "arial.ttf"
    
    title_font = ImageFont.truetype(font_bold, 56)
    header_font = ImageFont.truetype(font_bold, 42)
    body_font = ImageFont.truetype(font_reg, 36)
    sub_font = ImageFont.truetype(font_bold, 40)
    
    # Top Header
    draw.rectangle([0, 0, w, 140], fill=(22, 27, 34))
    draw.text((60, 45), "🐙 GITHUB REPO SHOWCASE", fill=(88, 166, 255), font=header_font)
    draw.text((w - 240, 45), str(repo_data.get("stars", "⭐")), fill=(227, 179, 65), font=header_font)
    
    if idx == 0:
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(22, 27, 34), outline=(48, 54, 61), width=3)
        draw.text((100, 320), "FEATURED REPOSITORY", fill=(139, 148, 158), font=body_font)
        draw.text((100, 400), repo_data["name"], fill=(88, 166, 255), font=title_font)
        draw.text((100, 520), repo_data.get("tagline", "")[:90], fill=(240, 246, 252), font=header_font)
        draw.rounded_rectangle([100, 720, 460, 810], radius=16, fill=(35, 134, 54))
        draw.text((130, 745), "⚡ 100% OPEN SOURCE", fill=(255, 255, 255), font=body_font)
    elif idx == 1:
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(1, 4, 9), outline=(48, 54, 61), width=3)
        draw.rounded_rectangle([60, 260, w - 60, 340], radius=24, fill=(22, 27, 34))
        draw.ellipse([90, 285, 115, 310], fill=(248, 81, 73))
        draw.ellipse([130, 285, 155, 310], fill=(227, 179, 65))
        draw.ellipse([170, 285, 195, 310], fill=(46, 160, 67))
        draw.text((230, 280), "Terminal / CLI Execution", fill=(139, 148, 158), font=body_font)
        draw.text((100, 400), f"$ {repo_data['command']}", fill=(63, 185, 80), font=header_font)
        draw.text((100, 540), ">>> Initializing local engine...", fill=(201, 209, 217), font=body_font)
        draw.text((100, 620), ">>> Execution successful (0.4s) 🚀", fill=(88, 166, 255), font=body_font)
    elif idx == 2:
        draw.text((60, 220), "🔥 TOP ADVANTAGES & PROS", fill=(46, 160, 67), font=title_font)
        y = 330
        for pro in repo_data["pros"]:
            draw.rounded_rectangle([60, y, w - 60, y + 160], radius=20, fill=(22, 27, 34), outline=(46, 160, 67), width=2)
            draw.text((100, y + 50), f"✅ {pro}", fill=(240, 246, 252), font=header_font)
            y += 200
    elif idx == 3:
        draw.text((60, 220), "⚠️ LIMITATIONS & CONS", fill=(248, 81, 73), font=title_font)
        y = 330
        for con in repo_data["cons"]:
            draw.rounded_rectangle([60, y, w - 60, y + 180], radius=20, fill=(22, 27, 34), outline=(248, 81, 73), width=2)
            draw.text((100, y + 60), f"❌ {con}", fill=(240, 246, 252), font=header_font)
            y += 220
    else:
        draw.rounded_rectangle([60, 260, w - 60, 950], radius=24, fill=(22, 27, 34), outline=(88, 166, 255), width=3)
        draw.text((120, 350), "🚀 WANT THE REPO LINK?", fill=(240, 246, 252), font=title_font)
        draw.text((120, 480), "💬 Comment 'REPO' below", fill=(88, 166, 255), font=header_font)
        draw.rounded_rectangle([120, 700, w - 120, 830], radius=20, fill=(31, 111, 235))
        draw.text((160, 740), "✨ FOLLOW FOR DAILY TECH", fill=(255, 255, 255), font=header_font)
        
    # Subtitle Box
    box_w, box_h = 980, 320
    box_x = (w - box_w) // 2
    box_y = h - box_h - 120
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=(1, 4, 9, 230), outline=(88, 166, 255), width=3)
    
    words = subtitle.split()
    lines, curr = [], []
    for word in words:
        test = " ".join(curr + [word])
        try:
            bbox = draw.textbbox((0, 0), test, font=sub_font)
            lw = bbox[2] - bbox[0]
        except AttributeError:
            lw = len(test) * 20
        if lw <= 880: curr.append(word)
        else:
            lines.append(" ".join(curr))
            curr = [word]
    if curr: lines.append(" ".join(curr))
    
    sub_y = box_y + 40
    for line in lines[:4]:
        try:
            bbox = draw.textbbox((0, 0), line, font=sub_font)
            lw = bbox[2] - bbox[0]
        except AttributeError:
            lw = len(line) * 20
        sx = (w - lw) // 2
        draw.text((sx + 2, sub_y + 2), line, fill=(0, 0, 0), font=sub_font)
        draw.text((sx, sub_y), line, fill=(255, 223, 0), font=sub_font)
        sub_y += 55
        
    canvas.save(out_path)

def zoom_frame(frame, t, duration, zoom_ratio=0.05):
    h, w, c = frame.shape
    scale = 1.0 + zoom_ratio * (t / duration)
    pil_img = Image.fromarray(frame)
    new_w, new_h = int(w * scale), int(h * scale)
    pil_resized = pil_img.resize((new_w, new_h), Image.Resampling.BILINEAR)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return np.array(pil_resized.crop((left, top, left + w, top + h)))

def build_video(repo_data, segments, audio_path, out_mp4):
    audio_clip = AudioFileClip(audio_path)
    dur = audio_clip.duration
    words_per_seg = [len(s.split()) for s in segments]
    total_words = sum(words_per_seg)
    clips, frames = [], []
    
    try:
        for i, seg in enumerate(segments):
            seg_dur = (words_per_seg[i] / total_words) * dur
            fpath = f"temp_scene_{i}.png"
            create_scene(i, repo_data, seg, fpath)
            frames.append(fpath)
            clip = ImageClip(fpath).with_duration(seg_dur)
            zoomed = clip.transform(lambda gf, t, d=seg_dur: zoom_frame(gf(t), t, d))
            clips.append(zoomed)
            
        final = concatenate_videoclips(clips, method="compose").with_audio(audio_clip)
        final.write_videofile(out_mp4, fps=24, codec="libx264", audio_codec="aac", logger=None)
    finally:
        for c in clips:
            try: c.close()
            except: pass
        try: final.close()
        except: pass
        try: audio_clip.close()
        except: pass
        for f in frames:
            if os.path.exists(f):
                try: os.remove(f)
                except: pass

def main():
    parser = argparse.ArgumentParser(description="AI Video Studio Studio CLI")
    parser.add_argument("--topic", type=str, default="ollama/ollama", help="GitHub repo name or topic")
    parser.add_argument("--output", type=str, help="Output MP4 file path")
    parser.add_argument("--voice", type=str, default="hi-IN-MadhurNeural", help="Edge TTS voice model")
    args = parser.parse_args()
    
    repo_data = fetch_live_github_info(args.topic)
    script, segments = generate_hindi_script(repo_data)
    
    downloads = os.path.join(os.path.expanduser('~'), 'Downloads')
    temp_audio = os.path.join(downloads, 'temp_audio.mp3')
    out_mp4 = args.output or os.path.join(downloads, 'output_reel.mp4')
    
    print(f"🎬 Producing 60-Second Video for '{repo_data['name']}'...")
    asyncio.run(generate_tts(script, temp_audio, args.voice))
    build_video(repo_data, segments, temp_audio, out_mp4)
    
    if os.path.exists(temp_audio):
        try: os.remove(temp_audio)
        except: pass
        
    print(f"✅ Video Complete: {out_mp4}")

if __name__ == "__main__":
    main()
