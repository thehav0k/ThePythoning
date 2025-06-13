## Music Player CLI

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # Hide the pygame welcome message
import yt_dlp
import pygame

# downloads audio from YouTube using yt-dlp
# must have ffmpeg installed
def download_audio(youtube_url, output_path='audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def play_with_controls(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    print("Commands: p = pause, r = resume, s = stop, q = quit")
    stopped = False
    paused = False
    while True:
        cmd = input("Enter command: ").strip().lower()
        if cmd == 'p':
            pygame.mixer.music.pause()
            paused = True
        elif cmd == 'r':
            pygame.mixer.music.unpause()
            paused = False
        elif cmd == 's':
            pygame.mixer.music.stop()
            stopped = True
            paused = False
        elif cmd == 'q':
            pygame.mixer.music.stop()
            break
        # If stopped, allow user to play again
        if stopped:
            again = input("Type 'play' to play again or 'q' to quit: ").strip().lower()
            if again == 'play':
                pygame.mixer.music.play()
                stopped = False
            elif again == 'q':
                break
        # Only exit if playback finished and not paused or stopped
        if not pygame.mixer.music.get_busy() and not stopped and not paused:
            print("Playback finished.")
            break
    pygame.mixer.quit()

if __name__ == '__main__':
    query = input('Enter YouTube URL or song name: ')
    if not (query.startswith('http://') or query.startswith('https://')):
        query = f'ytsearch1:{query}'
    base_audio_file = 'audio.mp3'
    download_audio(query, 'audio')
    if os.path.exists(base_audio_file):
        print(f'Playing: {base_audio_file}')
        play_with_controls(base_audio_file) # Play the downloaded audio file
        os.remove(base_audio_file) # gaan shona shesh, so delete it
    else:
        print('Audio file not found!')