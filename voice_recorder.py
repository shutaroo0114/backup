import sys
import pyaudio
import wave
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

class VoiceRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("音声録音アプリ")
        self.setFixedSize(200, 120)

        layout = QVBoxLayout()

        self.start_button = QPushButton("録音開始")
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("録音停止")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        self.recording = False
        self.frames = []

    def start_recording(self):
        self.recording = True
        self.frames = []
        self.thread = threading.Thread(target=self.record)
        self.thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.recording = False
        self.thread.join()
        self.save_audio()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def record(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024

        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                            input=True, frames_per_buffer=CHUNK)

        while self.recording:
            data = stream.read(CHUNK)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

    def save_audio(self):
        wf = wave.open("recorded.wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("保存しました → recorded.wav")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    recorder = VoiceRecorder()
    recorder.show()
    sys.exit(app.exec_())
