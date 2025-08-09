import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("画面音声キャプチャー録音アプリ")
        self.setGeometry(300, 300, 300, 120)

        self.layout = QVBoxLayout()

        self.label = QLabel("録音は停止中")
        self.layout.addWidget(self.label)

        self.start_btn = QPushButton("録音スタート")
        self.start_btn.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("録音ストップ")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)  # 最初は停止ボタン無効
        self.layout.addWidget(self.stop_btn)

        self.setLayout(self.layout)

        self.process = None  # 録音プロセス用

    def start_recording(self):
        # 下の monitor_name は「pactl list sources short」で調べて自分のに書き換えてね！
        monitor_name = "alsa_output.pci-0000_26_00.1.hdmi-stereo.monitor"

        command = f"parec --format=s16le --rate=44100 --channels=2 --device={monitor_name} | sox -t raw -r 44100 -e signed -b 16 -c 2 -V1 - ~/デスクトップ/youtube_audio.wav"
        self.process = subprocess.Popen(command, shell=True)
        
        self.label.setText("録音中...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_recording(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.label.setText("録音停止しました。\nデスクトップの youtube_audio.wav に保存されました。")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRecorder()
    window.show()
    sys.exit(app.exec_())
