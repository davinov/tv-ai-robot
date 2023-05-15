#!/bin/bash
cd /usr/share/robot-playlist
yt-dlp -f 'bestvideo[height<=576][ext=mp4]+bestaudio[ext=m4a]/best[height<=576]' --merge-output-format mp4 -o '%(title)s.%(ext)s' $1
