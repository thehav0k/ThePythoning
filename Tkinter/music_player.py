import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1" # Hide the pygame welcome message

import yt_dlp
import pygame
import threading
import tkinter as tk
from tkinter import ttk
import requests
import time
from PIL import Image, ImageTk
import io

AUDIO_FILE = 'audio.mp3'
playlist = []
current_index = 0
loop_enabled = False

def download_audio(youtube_url, output_path='audio'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'writethumbnail': True,
        'postprocessor_args': ['-loglevel', 'panic'],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        return info.get('title', 'Unknown Title'), info.get('thumbnail')

def format_time(seconds):
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02}:{int(sec):02}"

def gui_music_player():
    def play_song(index):
        global current_index
        if index < 0 or index >= len(playlist):
            return
        current_index = index
        query = playlist[index]
        status_var.set('🔄 Downloading...')
        disable_buttons()

        def task():
            try:
                q = f'ytsearch1:{query}' if not query.startswith('http') else query
                title, thumb_url = download_audio(q, 'audio')
                if os.path.exists(AUDIO_FILE):
                    status_var.set(f'▶️ Playing: {title}')
                    pygame.mixer.init()
                    pygame.mixer.music.load(AUDIO_FILE)
                    pygame.mixer.music.set_volume(volume_slider.get())
                    pygame.mixer.music.play()

                    try:
                        img_data = requests.get(thumb_url).content
                        img = Image.open(io.BytesIO(img_data)).resize((100, 100))
                        img = ImageTk.PhotoImage(img)
                        album_label.config(image=img)
                        album_label.image = img
                    except:
                        pass

                    update_buttons()

                    def update_seek():
                        while pygame.mixer.music.get_busy():
                            pos = pygame.mixer.music.get_pos() // 1000
                            seek_var.set(pos)
                            current_time_var.set(format_time(pos))
                            time.sleep(1)
                        if loop_enabled:
                            play_song(current_index)
                        else:
                            play_next()

                    threading.Thread(target=update_seek, daemon=True).start()
                else:
                    status_var.set('❌ Audio file not found!')
            except Exception as e:
                status_var.set(f'❗ Error: {e}')
                update_buttons()

        threading.Thread(target=task, daemon=True).start()

    def start_download_and_play():
        query = entry.get().strip()
        if not query:
            status_var.set('Please enter a song name or YouTube URL.')
            return
        playlist.append(query)
        play_song(len(playlist) - 1)

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
            os.remove(AUDIO_FILE)
        except:
            pass
        enable_play_button()

    def seek(val):
        pass  # Optional: Implement seek logic here

    def change_volume(val):
        volume = float(val)
        if pygame.mixer.get_init():
            pygame.mixer.music.set_volume(volume)

    def play_next():
        if current_index + 1 < len(playlist):
            play_song(current_index + 1)

    def play_previous():
        if current_index - 1 >= 0:
            play_song(current_index - 1)

    def toggle_loop():
        global loop_enabled
        loop_enabled = not loop_enabled
        loop_btn.config(bg='#00adb5' if loop_enabled else '#393e46')

    def disable_buttons():
        play_btn.config(state='disabled')
        pause_btn.config(state='disabled')
        resume_btn.config(state='disabled')
        stop_btn.config(state='disabled')

    def update_buttons():
        play_btn.config(state='disabled')
        pause_btn.config(state='normal')
        resume_btn.config(state='normal')
        stop_btn.config(state='normal')

    def enable_play_button():
        play_btn.config(state='normal')

    root = tk.Tk()
    root.title('🎶 YouTube Music Player')
    root.geometry('600x600')
    root.configure(bg='#222831')

    style = ttk.Style()
    style.configure("TScale", background="#222831", troughcolor="#393e46", sliderrelief='flat', sliderlength=15)

    # --- Top Search and Volume Layout ---
    top_frame = tk.Frame(root, bg='#222831')
    top_frame.pack(pady=(10, 0), fill='x')

    volume_frame = tk.Frame(top_frame, bg='#222831')
    volume_frame.pack(side='right', padx=15)
    tk.Label(volume_frame, text='🔊 Volume', bg='#222831', fg='white', font=('Arial', 10)).pack()
    volume_slider = ttk.Scale(volume_frame, from_=1.0, to=0.0, orient='vertical', length=100, command=change_volume)
    volume_slider.set(0.5)
    volume_slider.pack()

    tk.Label(top_frame, text='Enter YouTube URL or song name:', bg='#222831', fg='white', font=('Arial', 12)).pack(side='left', padx=10)
    entry = tk.Entry(top_frame, width=40, font=('Arial', 12))
    entry.pack(side='left', padx=5)

    # --- Album Art ---
    album_label = tk.Label(root, bg='#222831')
    album_label.pack(pady=10)

    # --- Status ---
    status_var = tk.StringVar(value='🎵 Ready.')
    tk.Label(root, textvariable=status_var, bg='#222831', fg='#ffd369', font=('Arial', 12, 'bold')).pack(pady=5)

    # --- Seek Bar (moved here) ---
    current_time_var = tk.StringVar(value='00:00')
    tk.Label(root, textvariable=current_time_var, font=('Arial', 10), bg='#222831', fg='white').pack()
    seek_var = tk.DoubleVar()
    seek_slider = ttk.Scale(root, from_=0, to=1000, variable=seek_var, orient='horizontal', length=480, command=seek)
    seek_slider.pack(pady=(0, 10))

    # --- Playback Controls ---
    btn_frame = tk.Frame(root, bg='#222831')
    btn_frame.pack(pady=10)

    button_args = {'font': ('Arial', 14), 'width': 4, 'bg': '#00adb5', 'fg': 'white', 'bd': 0, 'activebackground': '#007b80'}
    play_btn = tk.Button(btn_frame, text='▶️', command=start_download_and_play, **button_args)
    pause_btn = tk.Button(btn_frame, text='⏸️', command=pause, state='disabled', **button_args)
    resume_btn = tk.Button(btn_frame, text='⏯️', command=resume, state='disabled', **button_args)
    stop_btn = tk.Button(btn_frame, text='⏹️', command=stop, state='disabled', **button_args)
    prev_btn = tk.Button(btn_frame, text='⏮️', command=play_previous, **button_args)
    next_btn = tk.Button(btn_frame, text='⏭️', command=play_next, **button_args)
    loop_btn = tk.Button(btn_frame, text='🔁', command=toggle_loop, bg='#393e46', fg='white', bd=0)

    for i, btn in enumerate([play_btn, pause_btn, resume_btn, stop_btn, prev_btn, next_btn, loop_btn]):
        btn.grid(row=0, column=i, padx=4)

    root.mainloop()

if __name__ == '__main__':
    gui_music_player()