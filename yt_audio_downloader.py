import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import re
import threading
import yt_dlp
from yt_dlp.utils import DownloadError

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def read_links_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def get_unique_filename(output_dir, base_name):
    base = os.path.join(output_dir, base_name)
    file_path = base + ".mp3"
    count = 1
    while os.path.exists(file_path):
        file_path = f"{base}_{count}.mp3"
        count += 1
    return file_path

def bytes_to_mb(n):
    if n is None:
        return "?"
    return f"{n / (1024 * 1024):.2f} MB"

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes') or 0
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        percent = (downloaded / total * 100) if total else 0
        status_var.set(f"{bytes_to_mb(downloaded)} / {bytes_to_mb(total)} ({percent:.1f}%)")
        progress_bar["value"] = percent
        app.update_idletasks()

def download_audio(url, output_dir, index, total):
    try:
        ydl_opts_title = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts_title) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get('title', info.get('id')))
            safe_path = get_unique_filename(output_dir, title)

        if cancel_download:
            return False

        status_var.set(f"Downloading {index} of {total}: {title}")
        progress_bar["value"] = 0

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': safe_path.replace(".mp3", ".%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return True

    except DownloadError as e:
        messagebox.showerror("Invalid URL", f"Error on video {index} of {total}:\n{str(e)}")
        return True

    except Exception as e:
        status_var.set(f"Error on video {index} of {total}: {e}")
        return True

def start_download_thread():
    threading.Thread(target=start_download, daemon=True).start()

def start_download():
    global cancel_download
    cancel_download = False
    download_button.config(state="disabled")
    cancel_button.config(state="normal")

    if not app.link_file:
        messagebox.showerror("Error", "Please select a text file containing links.")
        return

    output_dir = filedialog.askdirectory(title="Select folder to save MP3 files")
    if not output_dir:
        return

    links = read_links_from_file(app.link_file)
    if not links:
        messagebox.showinfo("Info", "No links found in the selected file.")
        return

    total = len(links)
    progress_bar["maximum"] = 100
    progress_bar["value"] = 0

    for i, link in enumerate(links, start=1):
        if cancel_download:
            status_var.set(f"Download canceled at video {i} of {total}")
            break
        success = download_audio(link, output_dir, i, total)
        if not success:
            break

    if cancel_download:
        messagebox.showwarning("Canceled", "The download was canceled by the user.")
    else:
        status_var.set("All downloads completed successfully.")
        messagebox.showinfo("Done", "All MP3 files have been downloaded.")

    download_button.config(state="normal")
    cancel_button.config(state="disabled")

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        app.link_file = file_path
        file_label.config(text=f"Selected file: {os.path.basename(file_path)}")
        download_button.config(state="normal")

def cancel():
    global cancel_download
    cancel_download = True
    status_var.set("Cancelling download...")

# GUI setup
app = tk.Tk()
app.title("YouTube to MP3 Downloader")
app.geometry("600x300")
app.link_file = None
cancel_download = False

title = tk.Label(app, text="YouTube MP3 Downloader", font=("Helvetica", 14, "bold"))
title.pack(pady=10)

file_button = tk.Button(app, text="Select .txt File with YouTube Links", command=choose_file)
file_button.pack()

file_label = tk.Label(app, text="No file selected", fg="gray")
file_label.pack()

status_var = tk.StringVar()
status_label = tk.Label(app, textvariable=status_var, fg="blue", font=("Arial", 11))
status_label.pack(pady=10)

progress_bar = ttk.Progressbar(app, length=500, mode="determinate")
progress_bar.pack(pady=5)

btn_frame = tk.Frame(app)
btn_frame.pack(pady=10)

download_button = tk.Button(btn_frame, text="Start Download", bg="#4CAF50", fg="white", command=start_download_thread)
download_button.config(state="disabled")
download_button.pack(side="left", padx=10)

cancel_button = tk.Button(btn_frame, text="Cancel", bg="#f44336", fg="white", command=cancel, state="disabled")
cancel_button.pack(side="left", padx=10)

note_label = tk.Label(app, text="All MP3 files will be saved to a single folder.", font=("Arial", 9), fg="gray")
note_label.pack(pady=5)

app.mainloop()
