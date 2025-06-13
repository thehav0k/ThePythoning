## Music Player GUI

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # Hide the pygame welcome message
import yt_dlp
import pygame
import threading
import tkinter as tk

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

def gui_music_player():
    def start_download_and_play():
        query = entry.get().strip()
        if not query:
            status_var.set('Please enter a song name or YouTube URL.')
            return
        play_btn.config(state='disabled')
        pause_btn.config(state='normal')
        resume_btn.config(state='normal')
        stop_btn.config(state='normal')
        status_var.set('🔄 Downloading...')
        def task():
            q = query
            if not (q.startswith('http://') or q.startswith('https://')):
                q = f'ytsearch1:{q}'
            base_audio_file = 'audio.mp3'
            try:
                download_audio(q, 'audio')
                if os.path.exists(base_audio_file):
                    status_var.set('▶️ Playing...')
                    pygame.mixer.init()
                    pygame.mixer.music.load(base_audio_file)
                    pygame.mixer.music.play()
                else:
                    status_var.set('❌ Audio file not found!')
            except Exception as e:
                status_var.set(f'❗ Error: {e}')
        threading.Thread(target=task, daemon=True).start()

    def pause():
        pygame.mixer.music.pause()
        status_var.set('⏸️ Paused.')

    def resume():
        pygame.mixer.music.unpause()
        status_var.set('▶️ Playing...')

    def stop():
        pygame.mixer.music.stop()
        status_var.set('⏹️ Stopped.')
        try:
            os.remove('audio.mp3')
        except Exception:
            pass
        play_btn.config(state='normal')
        pause_btn.config(state='disabled')
        resume_btn.config(state='disabled')
        stop_btn.config(state='disabled')

    root = tk.Tk()
    root.title('YouTube Music Player')
    root.geometry('400x260')
    root.configure(bg='#222831')

    tk.Label(root, text='Enter YouTube URL or song name:', bg='#222831', fg='#eeeeee', font=('Arial', 12)).pack(pady=(15, 5))
    entry = tk.Entry(root, width=40, font=('Arial', 12))
    entry.pack(pady=5)

    btn_frame = tk.Frame(root, bg='#222831')
    btn_frame.pack(pady=10)

    play_btn = tk.Button(btn_frame, text='▶️', font=('Arial', 16), width=4, command=start_download_and_play, bg='#00adb5', fg='white', activebackground='#393e46', activeforeground='white', bd=0)
    play_btn.grid(row=0, column=0, padx=5)
    pause_btn = tk.Button(btn_frame, text='⏸️', font=('Arial', 16), width=4, command=pause, state='disabled', bg='#00adb5', fg='white', activebackground='#393e46', activeforeground='white', bd=0)
    pause_btn.grid(row=0, column=1, padx=5)
    resume_btn = tk.Button(btn_frame, text='⏯️', font=('Arial', 16), width=4, command=resume, state='disabled', bg='#00adb5', fg='white', activebackground='#393e46', activeforeground='white', bd=0)
    resume_btn.grid(row=0, column=2, padx=5)
    stop_btn = tk.Button(btn_frame, text='⏹️', font=('Arial', 16), width=4, command=stop, state='disabled', bg='#00adb5', fg='white', activebackground='#393e46', activeforeground='white', bd=0)
    stop_btn.grid(row=0, column=3, padx=5)

    status_var = tk.StringVar()
    status_var.set('🎵 Ready.')
    status_label = tk.Label(root, textvariable=status_var, bg='#222831', fg='#ffd369', font=('Arial', 12, 'bold'))
    status_label.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    gui_music_player()

#Absolute Cinema