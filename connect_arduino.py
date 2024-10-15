import serial
import serial.tools.list_ports
import re
import tkinter as tk
from tkinter import ttk, scrolledtext
import gas_api
import threading

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

def start_serial_communication(port):
    ser = serial.Serial(port, 115200)
    not_used = ser.readline()
    while True:
        val_arduino = ser.readline()
        decoded_str = val_arduino.decode('utf-8', errors='replace')
        converted_text = extract_and_convert(decoded_str)
        if converted_text:
            log_output(f"受信データ: {converted_text}")
            res = gas_api.send_GAS_API(converted_text)
            if res.status_code == 200:
                log_output('データを送信しました')

def log_output(message):
    text_area.insert(tk.END, message + '\n')
    text_area.see(tk.END)  # スクロールを最新のメッセージに合わせる

def select_port():
    port = port_combobox.get()
    log_output(f"選択したポート: {port}")
    # シリアル通信を別スレッドで開始
    threading.Thread(target=start_serial_communication, args=(port,), daemon=True).start()

if __name__ == '__main__':
    ports = [port.device for port in serial.tools.list_ports.comports()]

    # GUIの作成
    root = tk.Tk()
    root.title("シリアルポート選択")

    label = tk.Label(root, text="シリアルポートを選択してください:")
    label.pack(pady=10)

    port_combobox = ttk.Combobox(root, values=ports)
    port_combobox.pack(pady=10)

    select_button = tk.Button(root, text="選択", command=select_port)
    select_button.pack(pady=10)

    # ログ出力用のテキストエリア
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
    text_area.pack(pady=10)

    root.mainloop()