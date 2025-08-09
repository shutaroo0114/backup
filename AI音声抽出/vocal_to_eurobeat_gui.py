import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import subprocess

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vocal to Eurobeat Generator")
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()

        self.file_label = QLabel("音声ファイルを選択してください:")
        self.layout.addWidget(self.file_label)

        self.file_path = QLineEdit()
        self.layout.addWidget(self.file_path)

        self.browse_btn = QPushButton("参照")
        self.browse_btn.clicked.connect(self.browse_file)
        self.layout.addWidget(self.browse_btn)

        self.demucs_btn = QPushButton("1. ボーカルと伴奏を分離（Demucs）")
        self.demucs_btn.clicked.connect(self.run_demucs)
        self.layout.addWidget(self.demucs_btn)

        self.crepe_btn = QPushButton("2. 主旋律抽出（CREPE）")
        self.crepe_btn.clicked.connect(self.run_crepe)
        self.layout.addWidget(self.crepe_btn)

        self.generate_btn = QPushButton("3. ユーロビート風MIDI生成")
        self.generate_btn.clicked.connect(self.generate_midi)
        self.layout.addWidget(self.generate_btn)

        self.status = QTextEdit()
        self.status.setFont(QFont("Consolas", 10))
        self.status.setReadOnly(True)
        self.layout.addWidget(self.status)

        self.setLayout(self.layout)

    def log(self, message):
        self.status.append(f"[INFO] {message}")

    def browse_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "音声ファイルを選択", "", "Audio Files (*.wav *.mp3)")
        if fname:
            self.file_path.setText(fname)

    def run_demucs(self):
        path = self.file_path.text()
        if not path:
            self.log("音声ファイルが選択されていません")
            return
        self.log("Demucsで分離中...")
        os.makedirs("separated", exist_ok=True)
        command = f"demucs --two-stems=vocals -o separated \"{path}\""
        subprocess.run(command, shell=True)
        self.log("ボーカルと伴奏の分離が完了しました")

    def run_crepe(self):
        self.log("CREPEで主旋律抽出中...")
        os.system("python extract_melody_crepe.py")
        self.log("主旋律の抽出が完了しました")

    def generate_midi(self):
        self.log("ユーロビート風MIDIを生成中...")
        os.system("python generate_eurobeat_midi.py")
        self.log("MIDIファイルを生成しました: output.mid")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
