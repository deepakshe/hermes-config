#!/usr/bin/env python3
"""Verify Ollama + Hermes local setup for web scraping."""

import subprocess
import sys
import json

def check_ollama():
    """Check if Ollama is running and accessible."""
    print("=== Checking Ollama ===")
    try:
        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/tags"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            print("❌ Ollama not responding")
            return False
        data = json.loads(result.stdout)
        models = data.get("models", [])
        if not models:
            print("❌ No models found in Ollama")
            return False
        print(f"✅ Ollama running with {len(models)} model(s)")
        for m in models:
            name = m.get("name", "unknown")
            size_mb = m.get("size", 0) / (1024*1024)
            quant = m.get("details", {}).get("quantization_level", "unknown")
            print(f"   - {name}: {size_mb:.1f} MB, quant={quant}")
        return True
    except Exception as e:
        print(f"❌ Ollama check failed: {e}")
        return False

def check_hermes_config():
    """Check Hermes config points to local Ollama."""
    print("\n=== Checking Hermes Config ===")
    try:
        result = subprocess.run(
            ["hermes", "config", "show"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            print("❌ hermes config show failed")
            return False
        output = result.stdout
        # Check for key config items
        checks = {
            "provider: ollama": "provider: ollama" in output,
            "base_url: http": "base_url: http" in output,
            "default: hermes3:3b": "default: hermes3:3b" in output,
        }
        all_ok = True
        for desc, found in checks.items():
            status = "✅" if found else "❌"
            print(f"   {status} {desc}")
            if not found:
                all_ok = False
        return all_ok
    except Exception as e:
        print(f"❌ Hermes config check failed: {e}")
        return False

def main():
    ollama_ok = check_ollama()
    hermes_ok = check_hermes_config()
    
    print("\n" + "="*50)
    if ollama_ok and hermes_ok:
        print("✅ ALL CHECKS PASSED - Ready for web scraping!")
        print("Run: hermes chat -q \"Your web scraping task here\"")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Fix issues before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())