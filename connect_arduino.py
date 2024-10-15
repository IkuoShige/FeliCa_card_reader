import serial
import serial.tools.list_ports
import re
import tkinter as tk
from tkinter import ttk, scrolledtext
import gas_api
import threading
import yaml

def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config['url']

def save_config(url):
    with open('config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump({'url': url}, file, allow_unicode=True)

def hex_string_to_text(hex_string):
    hex_values = hex_string.split()
    text = ''.join(chr(int(h, 16)) for h in hex_values)
    return text

def extract_and_convert(output):
    match = re.search(r'読み取りデータ: (.+)', output)
    if match:
        hex_data = match.group(1)
        return hex_string_to_text(hex_data)
    return None

def start_serial_communication(port, url):
    ser = serial.Serial(port, 115200)
    not_used = ser.readline()
    while True:
        val_arduino = ser.readline()
        decoded_str = val_arduino.decode('utf-8', errors='replace')
        converted_text = extract_and_convert(decoded_str)
        if converted_text:
            log_output(f"受信データ: {converted_text}")
            res = gas_api.send_GAS_API(url, converted_text)
            if res.status_code == 200:
                log_output('データを送信しました')

def log_output(message):
    text_area.insert(tk.END, message + '\n')
    text_area.see(tk.END)  # スクロールを最新のメッセージに合わせる

def select_port():
    port = port_combobox.get()
    url = load_config()  # YAMLからURLを取得
    log_output(f"選択したポート: {port}")
    # log_output(f"使用するURL: {url}")
    # root.destroy()  # GUIを閉じる
    # シリアル通信を別スレッドで開始
    threading.Thread(target=start_serial_communication, args=(port, url), daemon=True).start()

def save_url():
    url = url_entry.get()
    save_config(url)
    log_output(f"URLを保存しました: {url}")

if __name__ == '__main__':
    ports = [port.device for port in serial.tools.list_ports.comports()]
    default_url = load_config()  # YAMLからURLを読み込む

    # GUIの作成
    root = tk.Tk()
    root.title("シリアルポート選択")

    # タブの作成
    tab_control = ttk.Notebook(root)
    
    # シリアルポート選択タブ
    port_tab = ttk.Frame(tab_control)
    tab_control.add(port_tab, text='シリアルポート選択')

    label = tk.Label(port_tab, text="シリアルポートを選択してください:")
    label.pack(pady=10)

    port_combobox = ttk.Combobox(port_tab, values=ports)
    port_combobox.pack(pady=10)

    select_button = tk.Button(port_tab, text="選択", command=select_port)
    select_button.pack(pady=10)

    # 設定タブ
    config_tab = ttk.Frame(tab_control)
    tab_control.add(config_tab, text='設定')

    url_label = tk.Label(config_tab, text="GAS APIのURLを入力してください:")
    url_label.pack(pady=10)

    url_entry = tk.Entry(config_tab, width=50)
    url_entry.pack(pady=10)
    url_entry.insert(0, default_url)  # デフォルトURLを表示

    save_button = tk.Button(config_tab, text="保存", command=save_url)
    save_button.pack(pady=10)

    # ログ出力用のテキストエリア
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
    text_area.pack(pady=10)

    tab_control.pack(expand=1, fill='both')
    root.mainloop()