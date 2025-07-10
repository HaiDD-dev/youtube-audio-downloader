
# YouTube MP3 Downloader

This is a Python desktop application that downloads audio (in MP3 format) from YouTube videos.  
It offers a straightforward graphical user interface (GUI) featuring a progress bar, detailed status updates, and the ability to cancel the download process at any time.

---

## 🎯 Features

- Read YouTube video links from a `.txt` file
- Download best-quality audio and convert to `.mp3` using `yt-dlp` and `ffmpeg`
- All MP3 files saved in a single folder
- Cancel button to stop the process mid-way
- Message box alerts when finished or canceled

---

## 🖼️ User Interface

- Button to choose a `.txt` file containing YouTube URLs
- Button to select the output folder
- Start and Cancel buttons
- Status label and progress bar
- Pop-up notifications on completion

---

## 📄 Example Input File

```txt
https://www.youtube.com/watch?v=VIDEO_ID_1
https://www.youtube.com/watch?v=VIDEO_ID_2
...
````

---

## 💾 Installation

Make sure you have **Python 3.7+** (supports Python 3.13) and the required libraries:

```bash
pip install yt-dlp
```

To enable audio conversion to MP3, you also need **ffmpeg**:

* [Install FFmpeg](https://ffmpeg.org/download.html)

Add `ffmpeg` to the system PATH so `yt-dlp` can use it.

---

## 🚀 How to Use

1. Run the Python script:

```bash
python yt_audio_downloader.py
```

2. Click **"Select .txt File with YouTube Links"**
3. Click **"Start Download"**
4. Choose the output folder
5. Monitor progress and status
6. Click **"Cancel"** anytime to stop

---

## 📁 Output Example

If your output folder is `C:\Music`, after downloading:

```
C:\Music\
├── Song_Title_1.mp3
├── Song_Title_2.mp3
```

File names are sanitized to remove invalid characters.

---

## 🛠 Dependencies

* `yt-dlp` – download and extract audio
* `ffmpeg` – used by `yt-dlp` to convert audio
* `tkinter` – built-in GUI module (no need to install)

---

## 📌 Notes

* Download is sequential (not parallel) to allow safe cancellation
* Duplicate video titles will be automatically renamed (`_1`, `_2`, ...)
* All downloads are `.mp3` at 192kbps (customizable in code)
