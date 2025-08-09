#!/bin/bash

# 仮想環境をアクティベート
source /home/shutaroo/デスクトップ/dance_analysis/.venv/bin/activate

# 処理1: GPU0 で動画フォルダ part1 を処理
CUDA_VISIBLE_DEVICES=0 python /home/shutaroo/デスクトップ/dance_analysis/batch_pose.py /home/shutaroo/デスクトップ/dance_analysis/videos_part1 &

# 処理2: GPU1 で動画フォルダ part2 を処理
CUDA_VISIBLE_DEVICES=1 python /home/shutaroo/デスクトップ/dance_analysis/batch_pose.py /home/shutaroo/デスクトップ/dance_analysis/videos_part2 &

# 両方の処理が終わるまで待つ
wait

echo "処理が終わりました。終了するにはEnterキーを押してください..."
read



