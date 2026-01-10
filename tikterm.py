#!/usr/bin/env python3
"""
TikTok Terminal Client - Play TikTok videos as ASCII art in your terminal
Uses yt-dlp for downloading (more reliable and Python 3.8 compatible)
"""

import os
import sys
import subprocess
import tempfile
import shutil


class TikTokTerminal:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        missing = []
        
        # Check for yt-dlp
        try:
            subprocess.run(['yt-dlp', '--version'], 
                         capture_output=True, check=False)
            print("✓ Found yt-dlp")
        except FileNotFoundError:
            print("❌ yt-dlp not found")
            missing.append("yt-dlp")
        
        # Check for mpv with ASCII support
        player = None
        try:
            result = subprocess.run(['mpv', '--vo=help'], 
                                  capture_output=True, text=True, check=False)
            if 'tct' in result.stdout:
                print("✓ Found mpv with tct support")
                player = 'mpv-tct'
            elif 'caca' in result.stdout:
                print("✓ Found mpv with caca support")
                player = 'mpv-caca'
            else:
                print("✓ Found mpv (but no ASCII renderers)")
        except FileNotFoundError:
            print("❌ mpv not found")
            missing.append("mpv")
        
        if missing:
            print("\n" + "="*50)
            print("Installation needed:")
            print("="*50)
            if "yt-dlp" in missing:
                print("\nFor yt-dlp:")
                print("  sudo apt install yt-dlp")
                print("  # or")
                print("  pip3 install yt-dlp --break-system-packages")
            if "mpv" in missing:
                print("\nFor mpv with ASCII support:")
                print("  sudo apt install mpv libcaca0 ffmpeg")
            return None
            
        return player
    
    def download_video(self, video_url):
        """Download TikTok video using yt-dlp"""
        print(f"\nDownloading video from {video_url}...")
        print("(This may take a moment...)")
        
        temp_file = os.path.join(self.temp_dir, 'tiktok_video.mp4')
        
        try:
            # Download with yt-dlp with progress
            result = subprocess.run([
                'yt-dlp',
                '-o', temp_file,
                '--progress',
                '--newline',
                video_url
            ], capture_output=False, text=True, timeout=60)
            
            if result.returncode != 0:
                print(f"❌ Download failed")
                return None
            
            if os.path.exists(temp_file):
                size = os.path.getsize(temp_file)
                print(f"✓ Downloaded: {size/1024:.1f} KB")
                return temp_file
            else:
                print("❌ Download failed - file not found")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"❌ Download timed out after 60 seconds")
            return None
        except Exception as e:
            print(f"❌ Error downloading video: {e}")
            return None
    
    def play_video(self, video_path, player='mpv-caca'):
        """Play video as ASCII art"""
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return
        
        print(f"\n{'='*50}")
        print(f"▶ Playing with {player}")
        print(f"{'='*50}")
        print("\nControls:")
        print("  q       - quit")
        print("  space   - pause/play")
        print("  ← →     - seek backward/forward")
        print("  [ ]     - decrease/increase speed")
        print(f"\n{'='*50}\n")
        
        try:
            if player == 'mpv-tct':
                subprocess.run(['mpv', '--vo=tct', video_path])
            elif player == 'mpv-caca':
                subprocess.run(['mpv', '--vo=caca', video_path])
            else:
                # Fallback to regular mpv
                subprocess.run(['mpv', video_path])
                
        except KeyboardInterrupt:
            print("\n\n⏹ Playback stopped.")
        except Exception as e:
            print(f"❌ Error playing video: {e}")
    
    def cleanup(self):
        """Clean up temp files"""
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass


def main():
    print("="*50)
    print("  TikTok Terminal Client (yt-dlp version)")
    print("="*50)
    
    client = TikTokTerminal()
    
    # Check dependencies
    player = client.check_dependencies()
    if not player:
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("\nUsage: python3 tikterm_ytdlp.py <tiktok_url>")
        print("\nExample:")
        print("  python3 tikterm_ytdlp.py https://www.tiktok.com/@user/video/123")
        sys.exit(1)
    
    video_url = sys.argv[1]
    
    # Download video
    video_path = client.download_video(video_url)
    
    if video_path:
        # Play video
        client.play_video(video_path, player)
    
    client.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)
