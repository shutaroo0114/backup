import os
import cv2
import sys
from multiprocessing import Process, Manager

def process_frames(frames, gpu_id, result_list, index, video_path):
    os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
    # ここに実際のGPU処理コードを書く。例としてフレーム番号を加工
    processed = [f"{os.path.basename(video_path)}_frame_{i}_gpu{gpu_id}" for i in frames]
    result_list[index] = processed

def main(video_path):
    if not os.path.exists(video_path):
        print("指定された動画ファイルが存在しません:", video_path)
        return
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    
    if total_frames == 0:
        print("動画のフレーム数が取得できません")
        return

    frames = list(range(total_frames))
    mid = total_frames // 2

    manager = Manager()
    results = manager.list([None, None])

    p1 = Process(target=process_frames, args=(frames[:mid], 0, results, 0, video_path))
    p2 = Process(target=process_frames, args=(frames[mid:], 1, results, 1, video_path))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    all_results = results[0] + results[1]
    print("処理結果:", all_results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python batch_pose_gpu_split.py <動画ファイルパス>")
    else:
        main(sys.argv[1])
