import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def run_processing():
    video_path = filedialog.askopenfilename(
        title="動画ファイルを選んでください",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if not video_path:
        return

    script_path = os.path.join(os.path.dirname(__file__), "batch_pose_gpu_split.py")
    cmd = ["/home/shutaroo/デスクトップ/dance_analysis/.venv/bin/python", script_path, video_path]

    try:
        subprocess.run(cmd, check=True)
        messagebox.showinfo("完了", "処理が終わりました！")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("エラー", f"処理でエラーが起きました:\n{e}")

root = tk.Tk()
root.title("ダンスGPUキャプチャー")

btn = tk.Button(root, text="動画選んで処理開始", command=run_processing, width=30, height=3)
btn.pack(pady=30)

root.mainloop()
