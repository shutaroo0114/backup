import os
import sys
import cv2
from mediapipe.python.solutions import pose

def main():
    if len(sys.argv) < 2:
        print("使い方: python batch_pose.py <動画フォルダのパス>")
        sys.exit(1)

    video_folder = sys.argv[1]

    if not os.path.exists(video_folder):
        print(f"指定されたフォルダがありません: {video_folder}")
        sys.exit(1)

    output_folder = os.path.join(video_folder, "output")
    os.makedirs(output_folder, exist_ok=True)

    # --- ここに動画ファイルの処理コードを追加 ---
    # 例としてフォルダ内のmp4動画を処理
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        print(f"処理中: {video_path}")
        # ここでMediaPipeを使って動画解析
        # 省略：あなたの既存処理を入れてください

    print("動画解析が完了しました。")

if __name__ == "__main__":
    main()

