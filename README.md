# 🎬 YouTube Transcript Downloader

A **GUI-based Python application** that allows users to download transcripts of YouTube videos by providing URLs. The application fetches the transcripts using the `youtube_transcript_api` library and saves them as a text file.

---

## 🚀 Features

✅ **Download YouTube Transcripts** - Fetches transcripts for multiple YouTube videos in one go.  
✅ **Batch Processing** - Supports multiple video URLs at once.  
✅ **User-Friendly GUI** - Built with **Tkinter**, making it easy to use.  
✅ **Custom Save Location & Filename** - Choose where to save the transcript and set a custom filename.  
✅ **Log Messages & Progress Bar** - Displays download progress and logs any errors.  

---

## 🛠️ Installation

### **🔹 Prerequisites**
Ensure you have **Python 3.x** installed on your system.

### **🔹 Install Dependencies**
Run the following command to install the required dependencies:

```bash
pip install tkinter youtube-transcript-api
```

---

## 📌 Usage

### **🔹 Run the Application**
To start the application, run:

```bash
python transcriptextractor.py
```

### **🔹 Steps to Use**
1. Enter **YouTube video links** (one per line).
2. Select the **save location** using the **Browse** button.
3. Enter a **filename** for the output transcript file.
4. Click **Download Transcripts** to start the process.
5. Wait for the progress bar to complete, and check the log messages for any errors.

---

## 📂 Output Format

The transcripts will be saved in a `.txt` file with the following structure:

```
--- Transcript for Video ID: XYZ123 ---
Transcript line 1
Transcript line 2
...
```

---

## 🛑 Error Handling

If an error occurs during processing (e.g., invalid link, transcript unavailable), the error message will be displayed in the log section.

---

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the project!

---

## 📜 License

This project is **open-source** and available under the **MIT License**.
