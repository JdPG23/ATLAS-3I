#!/usr/bin/env python3
"""
Script to generate the complete Comet 3I/ATLAS animation and video
This creates the full 400-frame cinematic animation
"""

import os
import subprocess
import sys

def run_animation():
    """Run the animation script to generate frames"""
    print("🎬 Generating Full Cinematic Animation (400 frames)...")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, 'comet_3i_animation.py'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("[SUCCESS] Animation frames generated successfully!")
            return True
        else:
            print("[ERROR] Animation generation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Failed to run animation script: {e}")
        return False

def create_video():
    """Create the final MP4 video"""
    print("\n🎥 Creating Final MP4 Video...")
    print("=" * 60)

    try:
        result = subprocess.run([sys.executable, 'create_video.py'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("[SUCCESS] Video created successfully!")
            return True
        else:
            print("[ERROR] Video creation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[ERROR] Failed to create video: {e}")
        return False

def main():
    print("🌟 COMET 3I/ATLAS - FINAL CINEMATIC ANIMATION GENERATOR 🌟")
    print("=" * 70)
    print("This will generate:")
    print("  • 400 high-quality animation frames")
    print("  • Cinematic MP4 video (26 seconds at 15fps)")
    print("  • Preview GIF")
    print("Estimated time: 10-15 minutes")
    print("=" * 70)

    # Step 1: Generate animation
    if not run_animation():
        print("\n❌ Animation generation failed. Cannot continue.")
        return False

    # Step 2: Create video
    if not create_video():
        print("\n❌ Video creation failed.")
        return False

    # Success summary
    print("\n" + "=" * 70)
    print("✨ SUCCESS! Final animation completed! ✨")
    print("=" * 70)
    print("📁 Files created in 'output/' folder:")
    print("   • comet_3i_atlas_cinematic.mp4 (MAIN VIDEO)")
    print("   • comet_3i_preview.gif (preview)")
    print("   • frame_*.png (individual frames)")
    print("")
    print("🎯 Ready for LinkedIn sharing!")
    print("   Use the text from linkedin_post.md")
    print("=" * 70)

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
