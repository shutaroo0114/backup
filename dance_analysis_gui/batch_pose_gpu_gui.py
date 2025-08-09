import os
import cv2
import tkinter as tk
from tkinter import filedialog
from multiprocessing import Process, Manager

def process_frames(frames, gpu_id, result_list, index):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    processed = [f"frame_{i}_gpu{gpu_id}" for i in frames]
    result_list[index] = processed

def main():
    # GUIで動画選択
    root = tk.Tk()
    root.withdraw()
    video_path = filedialog.askopenfilename(
        title="ダンス動画を選択してください",
        filetypes=[("動画ファイル", "*.mp4 *.avi *.mov")]
    )

    if not video_path:
        print("動画が選択されませんでした。終了します。")
        return

    # 動画読み込み
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print("動画のフレーム数が0です。パスまたはファイルを確認してください。")
        return

    frames = list(range(total_frames))
    mid = total_frames // 2

    manager = Manager()
    results = manager.list([None, None])

    # GPU0が前半処理
    p1 = Process(target=process_frames, args=(frames[:mid], 0, results, 0))
    # GPU1が後半処理
    p2 = Process(target=process_frames, args=(frames[mid:], 1, results, 1))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    all_results = results[0] + results[1]
    print("処理完了！総フレーム数:", len(all_results))

if __name__ == "__main__":
    main()
