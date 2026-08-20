import sys
import argparse
import asyncio
import edge_tts

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

async def main_async():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, required=True, help="Text to speak")
    parser.add_argument("--voice", type=str, default="hi-IN-MadhurNeural", help="Voice model")
    parser.add_argument("--output", type=str, required=True, help="Output MP3 path")
    args = parser.parse_args()
    
    print(f"Synthesizing audio with voice '{args.voice}'...")
    comm = edge_tts.Communicate(args.text, args.voice)
    await comm.save(args.output)
    print(f"Audio saved to: {args.output}")

if __name__ == "__main__":
    asyncio.run(main_async())
