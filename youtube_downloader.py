import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from pytube import YouTube
import threading
import time
import os
from pathlib import Path

def get_download_path():
    # This function returns the default downloads path for different operating systems
    return str(Path.home() / "Downloads")

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = percentage_of_completion
    progress_label.config(text=f"Download progress: {percentage_of_completion:.2f}%")
    root.update_idletasks()

def scroll_title(title):
    while True:
        full_title = f"Downloading: {title}"
        for i in range(len(full_title)):
            displayed_title = full_title[i:] + " " + full_title[:i]
            root.title(displayed_title)
            time.sleep(0.2)

def download_video(link):
    try:
        video = YouTube(link, on_progress_callback=progress_function)
        video_title = video.title
        thread = threading.Thread(target=scroll_title, args=(video_title,))
        thread.daemon = True
        thread.start()
        
        stream = video.streams.get_highest_resolution()
        output_textbox.insert(tk.END, f"Downloading: {link}\n")
        root.update_idletasks()
        download_path = get_download_path()
        stream.download(output_path=download_path)
        output_textbox.insert(tk.END, f"Download completed for: {link}\nSaved to: {download_path}\n")
    except Exception as e:
        output_textbox.insert(tk.END, f"Failed to download video for: {link}. Error: {e}\n")

def download_videos():
    urls = url_textbox.get("1.0", tk.END).strip().split("\n")
    for link in urls:
        link = link.strip()
        if link:
            download_video(link)
    messagebox.showinfo("Download Status", "Download process completed.")

# Create the main application window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create a label for instructions
instruction_label = tk.Label(root, text="Enter YouTube URLs (one per line):")
instruction_label.pack(pady=5)

# Create a textbox for entering URLs
url_textbox = scrolledtext.ScrolledText(root, width=50, height=10)
url_textbox.pack(pady=5)

# Create a progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)

# Create a label to show progress percentage
progress_label = tk.Label(root, text="Download progress: 0%")
progress_label.pack(pady=5)

# Create a button to start the download process
download_button = tk.Button(root, text="Download Videos", command=download_videos)
download_button.pack(pady=5)

# Create a textbox for displaying output messages
output_textbox = scrolledtext.ScrolledText(root, width=50, height=10, state=tk.DISABLED)
output_textbox.pack(pady=5)

# Enable the output textbox for writing messages
output_textbox.config(state=tk.NORMAL)

# Run the application
root.mainloop()
