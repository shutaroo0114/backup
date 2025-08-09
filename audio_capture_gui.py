import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox

class AudioCaptureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube音声キャプチャー")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("録音状態：停止中")
        self.layout.addWidget(self.label)

        self.start_btn = QPushButton("録音開始")
        self.start_btn.clicked.connect(self.start_recording)
        self.layout.addWidget(self.start_btn)

        self.stop_btn = QPushButton("録音停止")
        self.stop_btn.clicked.connect(self.stop_recording)
        self.stop_btn.setEnabled(False)  # 最初は停止ボタン無効
        self.layout.addWidget(self.stop_btn)

        self.setLayout(self.layout)

        self.process = None  # ffmpegプロセスを保存

    def start_recording(self):
        if self.process is None:
            cmd = [
                "ffmpeg",
                "-f", "pulse",
                "-i", "default",
                "-ac", "2",
                "-ar", "44100",
                "youtube_audio.wav"
            ]
            try:
                self.process = subprocess.Popen(cmd)
                self.label.setText("録音状態：録音中")
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"録音開始に失敗しました。\n{e}")

    def stop_recording(self):
        if self.process:
            self.process.terminate()  # ffmpegプロセス終了指示
            self.process.wait()
            self.process = None
            self.label.setText("録音状態：停止中")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            QMessageBox.information(self, "完了", "録音を停止しました。\nファイル：youtube_audio.wav")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioCaptureApp()
    window.show()
    sys.exit(app.exec_())
