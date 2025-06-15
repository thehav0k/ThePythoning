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
import json
import glob

current_audio_file: str  # tracks the currently playing audio file path
playlist_file = 'playlist.json'
playlist = []  # list of {'title': str, 'query': str}
current_index = 0
loop_enabled = False
entry: tk.Entry  # global entry widget

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
    global playlist, entry
    global current_audio_file
    playlist_file = 'playlist.json' # Load existing playlist if available
    try:
        with open(playlist_file, 'r') as f:
            playlist = json.load(f)
    except:
        playlist = []

    def play_song(index):
        global current_index, current_audio_file
        if index < 0 or index >= len(playlist):
            return
        current_index = index
        entry_item = playlist[index]
        query = entry_item.get('query') if isinstance(entry_item, dict) else entry_item
        status_var.set('🔄 Downloading...')
        disable_buttons()

        def task():
            try:
                # generate a unique filename base per song index
                base = f"audio_{index}"
                q = f'ytsearch1:{query}' if not query.startswith('http') else query
                title, thumb_url = download_audio(q, base)
                # set current audio path
                audio_path = f"{base}.mp3"
                current_audio_file = audio_path

                # override title with actual YouTube title via oEmbed for direct URLs
                if query.startswith('http'):
                    try:
                        oembed = requests.get('https://www.youtube.com/oembed', params={'url': query, 'format': 'json'}).json()
                        title = oembed.get('title', title)
                    except:
                        pass

                if os.path.exists(audio_path):
                    status_var.set(f'▶️ Playing: {title}')
                    pygame.mixer.init()
                    pygame.mixer.music.load(audio_path)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()

                    try:
                        img_data = requests.get(thumb_url).content
                        img = Image.open(io.BytesIO(img_data)).resize((100, 100))
                        img = ImageTk.PhotoImage(img)
                        album_label.config(image=img)  # type: ignore
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
        global entry
        query = entry.get().strip()
        if not query:
            status_var.set('Please enter a song name or YouTube URL.')
            return
        # search if not a URL to get real title
        title = query
        url = query
        if not query.startswith('http'):
            status_var.set('🔄 Searching...')
            try:
                ydl = yt_dlp.YoutubeDL({'quiet': True})
                info = ydl.extract_info(f'ytsearch1:{query}', download=False)
                e = info.get('entries', [None])[0]
                if e:
                    title = e.get('title')
                    url = e.get('webpage_url')
            except Exception as e:
                status_var.set(f'❗ Search error: {e}')
                return
        # if already in playlist, just play it
        for idx, item in enumerate(playlist):
            if item.get('query') == url:
                play_song(idx)
                return
        # add new song and play
        playlist.append({'title': title, 'query': url})
        playlist_listbox.insert('end', title)
        play_song(len(playlist) - 1)

    def pause():
        pygame.mixer.music.pause()
        status_var.set('⏸️ Paused.')

    def resume():
        pygame.mixer.music.unpause()
        status_var.set('▶️ Playing...')

    def stop():
        global current_audio_file
        pygame.mixer.music.stop()
        status_var.set('⏹️ Stopped.')
        # remove the last downloaded file
        try:
            if current_audio_file and os.path.exists(current_audio_file):
                os.remove(current_audio_file)
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

    def save_playlist():
        try:
            with open(playlist_file, 'w') as f:
                json.dump(playlist, f, indent=4)  # type: ignore
            status_var.set('💾 Playlist saved.')
        except Exception as e:
            status_var.set(f'❗ Can\'t save: {e}')

    def delete_song():
        idxs = playlist_listbox.curselection()
        if not idxs: return
        for i in reversed(idxs):
            playlist.pop(i)
            playlist_listbox.delete(i)
        status_var.set('🗑️ Song removed.')

    # search and add first YouTube result to playlist
    def search_songs():
        global entry
        q = entry.get().strip()
        if not q:
            status_var.set('Enter a query for search.')
            return
        status_var.set('🔄 Searching...')
        try:
            ydl = yt_dlp.YoutubeDL({'quiet': True})
            info = ydl.extract_info(f'ytsearch1:{q}', download=False)
            e = info.get('entries', [None])[0]
            if e:
                title = e.get('title')
                url = e.get('webpage_url')
                # prevent duplicates
                if any(item.get('query') == url for item in playlist):
                    status_var.set('⚠️ Already in playlist.')
                else:
                    playlist.insert(0, {'title': title, 'query': url})
                    playlist_listbox.insert(0, title)
                    status_var.set(f'✅ Added: {title}')
            else:
                status_var.set('❌ No results.')
        except Exception as e:
            status_var.set(f'❗ Search error: {e}')

    root = tk.Tk()
    root.title('🎶 YouTube Music Player')
    root.geometry('600x600')
    root.resizable(True, True)
    root.configure(bg='#222831')

    style = ttk.Style()
    style.configure("TScale", background="#222831", troughcolor="#393e46", sliderrelief='flat', sliderlength=15)

    # common button style
    button_args = {
        'font': ('Arial', 14),
        'width': 4,
        'bg': '#00adb5',
        'fg': 'white',
        'relief': 'raised',
        'bd': 2,
        'activebackground': '#007b80'
    }
    # --- Top Search and Volume Layout ---
    top_frame = tk.Frame(root, bg='#222831')
    top_frame.pack(pady=(10, 0), fill='x')
    # Search entry and button
    entry = tk.Entry(top_frame, font=('Arial', 14), width=40)
    entry.pack(side='left', padx=(10, 5), expand=True, fill='x')
    search_btn = tk.Button(top_frame, text='🔍', command=search_songs, **button_args)
    search_btn.pack(side='left', padx=5)

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

    # --- Playlist ---
    tk.Label(root, text='Playlist:', bg='#222831', fg='white', font=('Arial', 12)).pack()
    playlist_listbox = tk.Listbox(root, width=50, bg='#393e46', fg='white', selectbackground='#00adb5', bd=0, highlightthickness=0)
    playlist_listbox.pack(pady=(0, 10), fill='both', expand=True)
    for item in playlist:
        playlist_listbox.insert('end', item.get('title', item))
    playlist_listbox.bind('<Double-1>', lambda e: play_song(playlist_listbox.curselection()[0]) if playlist_listbox.curselection() else None)
    playlist_btn_frame = tk.Frame(root, bg='#222831')
    playlist_btn_frame.pack(fill='x', pady=(0,10))
    save_btn = tk.Button(playlist_btn_frame, text='💾', command=save_playlist, **button_args)
    delete_btn = tk.Button(playlist_btn_frame, text='❌', command=delete_song, **button_args)
    save_btn.grid(row=0, column=0, padx=5)
    delete_btn.grid(row=0, column=1, padx=5)

    # --- Playback Controls ---
    btn_frame = tk.Frame(root, bg='#222831')
    btn_frame.pack(pady=10, fill='x')

    play_btn = tk.Button(btn_frame, text='▶️', command=start_download_and_play, **button_args)
    pause_btn = tk.Button(btn_frame, text='⏸️', command=pause, state='disabled', **button_args)
    resume_btn = tk.Button(btn_frame, text='⏯️', command=resume, state='disabled', **button_args)
    stop_btn = tk.Button(btn_frame, text='⏹️', command=stop, state='disabled', **button_args)
    prev_btn = tk.Button(btn_frame, text='⏮️', command=play_previous, **button_args)
    next_btn = tk.Button(btn_frame, text='⏭️', command=play_next, **button_args)
    loop_btn = tk.Button(btn_frame, text='🔁', command=toggle_loop, bg='#393e46', fg='white', bd=0)

    for i, btn in enumerate([play_btn, pause_btn, resume_btn, stop_btn, prev_btn, next_btn, loop_btn]):
        btn.grid(row=0, column=i, padx=4)

    # cleanup files on close
    def on_closing():
        try:
            pygame.mixer.music.stop()
        except:
            pass
        # delete downloaded audio and thumbnails
        patterns = ["audio_*.mp3", "audio_*.webp", "audio_*.jpg", "audio_*.png"]
        for pat in patterns:
            for f in glob.glob(pat):
                try:
                    os.remove(f)
                except:
                    pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == '__main__':
    gui_music_player()