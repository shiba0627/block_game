import serial
import time
from config import COM

def init_serial():
    print('Aruduinoと接続中...')
    global ser
    ser = serial.Serial(COM, 38400, timeout=1)
    time.sleep(2)
    print('接続完了')

def read_contller():
    x, y, a, b = joystick_read()
    if x < 256:
        print('left')
        return 0, a, b
    elif x > 768:
        print('right')
        return 2, a, b
    else:
        print('center')
        return 1, a, b
    
def joystick_read():
    ser.write(b'a')#コントローラーの状態要求コマンド
    xdata = ser.read(2)# 2バイト受信, ジョイスティックX軸の値
    ydata = ser.read(2)# 2バイト受信, ジョイスティックY軸の値
    button1 = ser.read(1)# 1バイト受信, ボタン1の状態
    button2 = ser.read(1)# 1バイト受信, ボタン2の状態
    reply_read()#NACKorACKを読み取り

    #初期値の設定
    x = 0
    y = 0
    button1_state = -1#0:押されている, 1:押されていない, -1:未受信
    button2_state = -1

    #X軸
    if len(xdata) == 2:
        x = (xdata[0] << 8) | xdata[1]  # 上位バイトを8bitシフトし、下位バイトと論理和をとる
    else:
        print("X軸データ受信失敗")

    #Y軸
    if len(ydata) == 2:
        y = (ydata[0] << 8) | ydata[1]
    else:
        print("Y軸データ受信失敗")

    #ボタン1
    if len(button1) == 1:
        button1_state = button1[0]
    else:
        print("ボタン1データ受信失敗")

    #ボタン2
    if len(button2) == 1:
        button2_state = button2[0]
    else:
        print("ボタン2データ受信失敗")

    return x, y, button1_state, button2_state

def LED_0():
    command = b'b'
    count = b'0'
    ser.write(command+count)
    reply_read()    

def LED_1():
    command = b'b'
    count = b'1'
    ser.write(command+count)
    reply_read()    

def LED_2():
    command = b'b'
    count = b'2'
    ser.write(command+count)
    reply_read()    

def LED_3():
    command = b'b'
    count = b'3'
    ser.write(command+count)
    reply_read()    

def reply_read():
    reply = ser.read(1)
    if reply == b'\x06':
        print("ACK")
    elif reply == b'\x15':
        print("NACK")
    else:
        print("Unknown response")
def serial_close():
    ser.close()
    print('Serial port closed')

def main():
    init_serial()
    print('q: 終了, a: ジョイスティックの値取得, 0-3: LED点灯')
    try:
        while True:
            key = input("> ")
            if key == 'q':
                print('終了')
                break
            elif key == 'a':
                x, y, a, b = joystick_read()
                print(f'(x,y)=({x},{y}), a:{a},b:{b}')
            elif key == '0':
                LED_0()
            elif key == '1':
                LED_1()
            elif key == '2':
                LED_2()
            elif key == '3':
                LED_3()  
    except KeyboardInterrupt:
            print('通信終了')
    finally:
        ser.close()
        print('Serial port closed')

if __name__ == '__main__':
    print('キーボード入力でArduinoと通信テスト')
    main()