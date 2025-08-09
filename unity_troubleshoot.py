import sys  # Pythonのシステム関連機能を使うためのモジュール
import os   # OSのファイルパスやファイル操作に使うモジュール
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QLabel, QMessageBox

class TroubleshootApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unity Hub トラブルシューティング支援ツール")
        self.resize(500, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("操作を選んでボタンを押してください")
        self.layout.addWidget(self.label)

        self.check_env_btn = QPushButton("環境チェック")
        self.check_env_btn.clicked.connect(self.check_environment)
        self.layout.addWidget(self.check_env_btn)

        self.clear_cache_btn = QPushButton("キャッシュクリア（簡易）")
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        self.layout.addWidget(self.clear_cache_btn)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.layout.addWidget(self.log_area)

        self.setLayout(self.layout)

    def check_environment(self):
        self.log_area.append("=== 環境チェック開始 ===")

        possible_path = os.path.expandvars(r"%LOCALAPPDATA%\UnityHub\UnityHub.exe")
        if os.path.exists(possible_path):
            self.log_area.append(f"Unity Hub 実行ファイル発見: {possible_path}")
            self.log_area.append("Unity Hub はインストールされています。")
        else:
            self.log_area.append("Unity Hub 実行ファイルが見つかりません。")

        self.log_area.append("=== 環境チェック終了 ===\n")

    def clear_cache(self):
        reply = QMessageBox.question(self, '確認', '本当にキャッシュを削除しますか？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.log_area.append("=== キャッシュ削除開始 ===")

            cache_path = os.path.expandvars(r"%LOCALAPPDATA%\UnityHub\Cache")
            if os.path.exists(cache_path):
                try:
                    for root, dirs, files in os.walk(cache_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            os.remove(file_path)
                            self.log_area.append(f"削除: {file_path}")
                    self.log_area.append("キャッシュを削除しました。")
                except Exception as e:
                    self.log_area.append(f"エラーが発生しました: {e}")
            else:
                self.log_area.append("キャッシュフォルダが見つかりません。")

            self.log_area.append("=== キャッシュ削除終了 ===\n")
        else:
            self.log_area.append("キャッシュ削除をキャンセルしました。\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TroubleshootApp()
    window.show()
    sys.exit(app.exec_())
