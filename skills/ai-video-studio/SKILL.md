---
name: ai-video-studio
description: Autonomous AI Video & Audio Production Studio. Generates 60-second Hindi/English tech Reels, fetches live GitHub repositories, renders neural voiceovers with Edge-TTS, and triggers n8n automated publishing pipelines.
---

# AI Video Studio Skill

This global skill equips Antigravity with full-stack automated video production, Hindi neural audio synthesis, live GitHub repository research, and n8n webhook orchestration.

## Capabilities

1. **Full-Pipeline Video Creation**:
   Generate 60-second vertical reels (1080x1920) with synchronized Hindi neural voiceover, multi-scene visual cards (terminal execution, pros, cons, outro), and word-level subtitles.
   ```bash
   python "C:/Users/admin/.gemini/config/skills/ai-video-studio/scripts/create-video.py" --topic "ollama" --lang "hindi"
   ```

2. **Live GitHub Repository Researcher**:
   Fetch real-time stars, descriptions, and README summaries for any GitHub repository to create accurate video scripts.
   ```bash
   python "C:/Users/admin/.gemini/config/skills/ai-video-studio/scripts/research-repo.py" --repo "ollama/ollama"
   ```

3. **Standalone Neural Voice Synthesizer (TTS)**:
   Generate instant high-fidelity audio files in Hindi (`hi-IN-MadhurNeural`) or English (`en-IN-NeerjaNeural`).
   ```bash
   python "C:/Users/admin/.gemini/config/skills/ai-video-studio/scripts/generate-audio.py" --text "Namaste dosto!" --voice "hi-IN-MadhurNeural" --output "C:/Users/admin/Downloads/voice.mp3"
   ```

4. **Trigger n8n Video Pipelines**:
   Fire the local n8n Docker workflow directly from Antigravity.
   ```powershell
   powershell -File "C:/Users/admin/.gemini/config/skills/ai-video-studio/scripts/trigger-n8n.ps1" -Topic "DeepSeek-R1"
   ```

## Directory Structure
- `scripts/create-video.py` — Core 5-scene MoviePy video engine.
- `scripts/research-repo.py` — GitHub API inspector.
- `scripts/generate-audio.py` — Edge-TTS voiceover engine.
- `scripts/trigger-n8n.ps1` — n8n Webhook trigger utility.
