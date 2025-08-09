from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from pytube import YouTube
import sys

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube 単体動画ダウンローダー")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("動画のURLをここに貼ってください")

        self.status_label = QLabel("")

        self.download_button = QPushButton("ダウンロード")
        self.download_button.clicked.connect(self.download_video)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("YouTube動画URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.download_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text()
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            self.status_label.setText("ダウンロード成功！")
        except Exception as e:
            self.status_label.setText(f"エラー: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
