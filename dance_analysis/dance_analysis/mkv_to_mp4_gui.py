import PySimpleGUI as sg
import subprocess
import os

def convert_mkv_to_mp4(input_path, output_path):
    # ffmpegコマンド実行
    command = ['ffmpeg', '-i', input_path, '-codec', 'copy', output_path]
    try:
        subprocess.run(command, check=True)
        return True, "変換成功！"
    except subprocess.CalledProcessError as e:
        return False, f"変換失敗: {e}"

# GUIレイアウト
layout = [
    [sg.Text('MKVファイルを選択してください')],
    [sg.InputText(key='-IN-'), sg.FileBrowse(file_types=(("MKV Files", "*.mkv"),))],
    [sg.Text('保存先ファイル名を指定してください')],
    [sg.InputText(key='-OUT-'), sg.FolderBrowse()],
    [sg.Button('変換開始'), sg.Button('終了')],
    [sg.Text('', key='-STATUS-', size=(40,2))]
]

window = sg.Window('MKV → MP4 変換アプリ', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == '終了':
        break

    if event == '変換開始':
        input_file = values['-IN-']
        output_folder = values['-OUT-']

        if not input_file or not output_folder:
            window['-STATUS-'].update('入力ファイルと保存先を指定してください')
            continue

        # 出力ファイル名をinputのファイル名から.mp4に変換
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, base_name + '.mp4')

        window['-STATUS-'].update('変換中…少し待ってね')

        success, message = convert_mkv_to_mp4(input_file, output_file)
        window['-STATUS-'].update(message)

window.close()

