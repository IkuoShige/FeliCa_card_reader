import serial
import re
import gas_api

def hex_string_to_text(hex_string):
    # 16進数の文字列をスペースで分割
    hex_values = hex_string.split()
    
    # 各16進数を文字に変換
    text = ''.join(chr(int(h, 16)) for h in hex_values)
    
    return text

def extract_and_convert(output):
    # 出力からデータを抽出
    match = re.search(r'読み取りデータ: (.+)', output)
    if match:
        hex_data = match.group(1)  # マッチした部分を取得
        return hex_string_to_text(hex_data)  # 16進数をテキストに変換
    return None


if __name__ == '__main__':
    #ser = serial.Serial('/dev/ttyACM0', 115200)
    ser = serial.Serial('COM3', 115200)
    not_used = ser.readline()
    while True:
        val_arduino = ser.readline()
        val_decoded = val_arduino
        decoded_str = val_decoded.decode('utf-8', errors='replace')
        converted_text = extract_and_convert(decoded_str)
        if converted_text:
            print(converted_text)
            gas_api.send_GAS_API(converted_text)
    ser.close()
