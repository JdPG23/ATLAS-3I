#!/usr/bin/env python3
"""
Script to create MP4 video from animation frames
Run this after the animation script has generated the frames
"""

import os
import subprocess
import sys

def create_mp4_from_frames():
    """Create MP4 video from PNG frames using ffmpeg"""

    frames_dir = 'output'
    output_file = 'output/comet_3i_atlas_cinematic.mp4'

    if not os.path.exists(frames_dir):
        print("[ERROR] '{frames_dir}' directory not found!")
        print("   Please run the animation script first to generate frames.")
        return False

    # Check for frame files
    frame_pattern = os.path.join(frames_dir, 'frame_%04d.png')
    test_frame = os.path.join(frames_dir, 'frame_0000.png')

    if not os.path.exists(test_frame):
        print("[ERROR] No frame files found in '{frames_dir}'!")
        print("   Please run the animation script first to generate frames.")
        return False

    # Count frames
    frame_count = len([f for f in os.listdir(frames_dir) if f.startswith('frame_') and f.endswith('.png')])
    print(f"[INFO] Found {frame_count} frames")

    # Use local ffmpeg executable
    ffmpeg_path = os.path.join('ffmpeg-master-latest-win64-gpl-shared', 'ffmpeg-master-latest-win64-gpl-shared', 'bin', 'ffmpeg.exe')

    if not os.path.exists(ffmpeg_path):
        print("[ERROR] ffmpeg.exe not found in expected location!")
        print(f"   Expected: {ffmpeg_path}")
        return False

    # Try to create video
    try:
        cmd = [
            ffmpeg_path,
            '-framerate', '30',  # Increased to 30 fps for smoother playback
            '-i', frame_pattern,
            '-vf', 'scale=1400:1000:force_original_aspect_ratio=decrease,pad=1400:1000:(ow-iw)/2:(oh-ih)/2',  # Force even dimensions
            '-c:v', 'libx264',
            '-crf', '18',
            '-preset', 'slow',
            '-pix_fmt', 'yuv420p',
            output_file,
            '-y'  # Overwrite output file
        ]

        print("[VIDEO] Creating MP4 video...")
        print(f"   Using ffmpeg from: {ffmpeg_path}")
        print("   This may take a few minutes...")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("[SUCCESS] MP4 video created successfully!")
            print(f"   File: {output_file}")
            return True
        else:
            print("[ERROR] ffmpeg failed with error:")
            print(f"   {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def create_gif_from_frames():
    """Create GIF from PNG frames as fallback"""

    frames_dir = 'output'
    output_file = 'output/comet_3i_atlas_animation.gif'

    if not os.path.exists(frames_dir):
        print(f"[ERROR] '{frames_dir}' directory not found!")
        return False

    # Use local ffmpeg executable
    ffmpeg_path = os.path.join('ffmpeg-master-latest-win64-gpl-shared', 'ffmpeg-master-latest-win64-gpl-shared', 'bin', 'ffmpeg.exe')

    if not os.path.exists(ffmpeg_path):
        print("[ERROR] ffmpeg.exe not found in expected location!")
        return False

    frame_pattern = os.path.join(frames_dir, 'frame_%04d.png')

    try:
        cmd = [
            ffmpeg_path,
            '-framerate', '10',
            '-i', frame_pattern,
            '-vf', 'scale=800:-1',
            output_file,
            '-y'
        ]

        print("[GIF] Creating GIF animation...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("[SUCCESS] GIF created successfully!")
            print(f"   File: {output_file}")
            return True
        else:
            print("[ERROR] GIF creation failed:")
            print(f"   {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] GIF creation error: {e}")
        return False

if __name__ == '__main__':
    print("[VIDEO CREATOR] Comet 3I/ATLAS Video Creator")
    print("=" * 50)

    # Try to create MP4 first
    if not create_mp4_from_frames():
        print("\n[FALLBACK] Trying to create GIF instead...")
        create_gif_from_frames()

    print("\n[INFO] Alternative: You can also use the frames to create videos online")
    print("   at sites like: ezgif.com, cloudconvert.com, or similar")

    print("\n[DONE] Video creation process completed!")
