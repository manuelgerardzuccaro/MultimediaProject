import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from stabilize import stabilize_video
from remove_artifacts import remove_artifacts
import cv2
from PIL import Image, ImageTk

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def process_video():
    input_path = entry_file_path.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".avi",
                                               filetypes=[("AVI files", "*.avi"), ("All files", "*.*")])
    if not input_path or not output_path:
        return

    stabilize_video(input_path, output_path)
    remove_artifacts(output_path, output_path)  # For simplicity, reprocess the same output file
    show_preview(output_path)

def show_preview(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video_preview.imgtk = imgtk
        lbl_video_preview.configure(image=imgtk)
    cap.release()

root = tk.Tk()
root.title("Video Stabilization and Artifact Removal")

frame_top = ttk.Frame(root)
frame_top.pack(pady=10)

lbl_file_path = ttk.Label(frame_top, text="Video File:")
lbl_file_path.pack(side=tk.LEFT)

entry_file_path = ttk.Entry(frame_top, width=50)
entry_file_path.pack(side=tk.LEFT, padx=5)

btn_browse = ttk.Button(frame_top, text="Browse", command=open_file)
btn_browse.pack(side=tk.LEFT)

frame_middle = ttk.Frame(root)
frame_middle.pack(pady=10)

btn_process = ttk.Button(frame_middle, text="Process Video", command=process_video)
btn_process.pack()

lbl_video_preview = ttk.Label(root)
lbl_video_preview.pack(pady=10)

root.mainloop()
