A CLI that downloads TikTok videos, converts to ASCII art, and plays in the terminal.

Pretty simple:
# Install yt-dlp
sudo apt install yt-dlp
# or
pip3 install yt-dlp --break-system-packages

# Install mpv with ASCII support
sudo apt install mpv libcaca0 ffmpeg

Usage: python3 tikterm.py https://www.tiktok.com/@zachking/video/7593008028077542670 best


Note that the ASCII art video needs a terminal that can handle:

Fast refresh rates
Proper color rendering (256 colors or truecolor)
Good Unicode support

Find me @h45hb4ng or more of my work at morallyrelative.com
