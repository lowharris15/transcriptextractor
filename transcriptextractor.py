import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import re
import threading
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeTranscriptDownloader:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Transcript Downloader")
        master.geometry("600x700")

        # YouTube Links Input
        self.links_label = tk.Label(master, text="YouTube Video Links (one per line):")
        self.links_label.pack(pady=(10, 0))

        self.links_text = tk.Text(master, height=10, width=70)
        self.links_text.pack(pady=10)

        # Save Location
        self.save_frame = tk.Frame(master)
        self.save_frame.pack(fill='x', padx=20, pady=10)

        self.save_path_var = tk.StringVar()
        self.save_path_entry = tk.Entry(self.save_frame, textvariable=self.save_path_var, width=50)
        self.save_path_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0, 10))

        self.browse_button = tk.Button(self.save_frame, text="Browse", command=self.browse_save_location)
        self.browse_button.pack(side=tk.RIGHT)

        # Filename Input
        self.filename_frame = tk.Frame(master)
        self.filename_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(self.filename_frame, text="Filename:").pack(side=tk.LEFT)
        self.filename_var = tk.StringVar(value="youtube_transcripts.txt")
        self.filename_entry = tk.Entry(self.filename_frame, textvariable=self.filename_var, width=30)
        self.filename_entry.pack(side=tk.LEFT, padx=10, expand=True, fill='x')

        # Download Button
        self.download_button = tk.Button(master, text="Download Transcripts", command=self.start_download)
        self.download_button.pack(pady=10)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = tk.ttk.Progressbar(master, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', padx=20, pady=10)

        # Log Area
        self.log_label = tk.Label(master, text="Logs:")
        self.log_label.pack()

        self.log_text = scrolledtext.ScrolledText(master, height=10, width=70, state='disabled')
        self.log_text.pack(padx=20, pady=10)

    def browse_save_location(self):
        """Open directory selection dialog"""
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.save_path_var.set(selected_dir)

    def log_message(self, message):
        """Add message to log text area"""
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.yview(tk.END)

    def extract_video_id(self, url):
        """Extract YouTube video ID from various URL formats"""
        # Regular expressions to match different YouTube URL formats
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\s]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\s]+)',
            r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^&\s]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract video ID from {url}")

    def download_transcripts(self, filename):
        """Main download process"""
        # Get links and save path
        links = [link.strip() for link in self.links_text.get("1.0", tk.END).split("\n") if link.strip()]
        save_path = self.save_path_var.get()

        # Validate inputs
        if not links:
            messagebox.showerror("Error", "Please enter YouTube video links")
            return
        if not save_path:
            messagebox.showerror("Error", "Please select a save location")
            return

        # Ensure .txt extension
        if not filename.lower().endswith('.txt'):
            filename += '.txt'

        # Full file path
        full_filepath = os.path.join(save_path, filename)

        # Reset progress
        self.progress_var.set(0)
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.configure(state='disabled')

        # Total links for progress calculation
        total_links = len(links)

        # Prepare to write all transcripts to a single file
        try:
            with open(full_filepath, 'w', encoding='utf-8') as outfile:
                # Process each link
                for index, link in enumerate(links, 1):
                    try:
                        # Extract video ID
                        video_id = self.extract_video_id(link)

                        # Log processing
                        self.log_message(f"Processing video ID: {video_id}")

                        # Write video separator
                        outfile.write(f"\n--- Transcript for Video ID: {video_id} ---\n\n")

                        # Get transcript
                        transcript = YouTubeTranscriptApi.get_transcript(video_id)

                        # Write transcript
                        for entry in transcript:
                            outfile.write(entry['text'] + '\n')

                        # Update progress
                        progress = (index / total_links) * 100
                        self.progress_var.set(progress)
                        self.log_message(f"Added transcript for video ID: {video_id}")

                    except Exception as e:
                        self.log_message(f"Error processing {link}: {str(e)}")

            # Completion message
            self.log_message(f"Transcripts saved to: {full_filepath}")
            messagebox.showinfo("Success", f"Transcripts downloaded to:\n{full_filepath}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save transcripts: {str(e)}")

    def start_download(self):
        """Start download in a separate thread"""
        # Get filename from entry
        filename = self.filename_var.get().strip()
        
        # Validate filename
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return

        # Start download in a separate thread
        download_thread = threading.Thread(target=self.download_transcripts, args=(filename,))
        download_thread.start()

def main():
    root = tk.Tk()
    import tkinter.ttk as ttk  # For progress bar
    app = YouTubeTranscriptDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()